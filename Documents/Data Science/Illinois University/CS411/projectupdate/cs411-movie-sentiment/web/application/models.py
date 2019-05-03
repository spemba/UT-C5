from application import app
from itertools import chain
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Connect to the database.
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=app.config['PGDEBUGMODE'])

class Movie:
    """
    Performs a movie search and enables movie CRUD operations.
    """

    _primary_key = {'tconst'}
    _column_set = {'tconst', 'titletype', 'primarytitle', 'originaltitle', 'isadult', 'startyear', 'endyear', 'runtimeminutes', 'genres'}

    def __init__(self, tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres):
        self.tconst = tconst
        self.titletype = titletype
        self.primarytitle = primarytitle
        self.originaltitle = originaltitle
        self.isadult = isadult
        self.startyear = startyear
        self.endyear = endyear
        self.runtimeminutes = runtimeminutes
        self.genres = genres

    @classmethod
    def get_all(cls, limit):
        result = engine.execute(text("SELECT * FROM movies LIMIT :limit"), limit=limit)
        return cls._unmarshall_many(result)

    @classmethod
    def get(cls, tconst):
        result = engine.execute(text("SELECT * FROM movies WHERE tconst = :tconst LIMIT 1"), tconst=tconst)
        return cls._unmarshall_many(result)

    @classmethod
    def get_random(cls):
        max_tconst = int(engine.scalar(text('SELECT SUBSTRING(MAX(tconst), 3) from movies')))
        random_tconst = 'tt%s' % randint(1, max_tconst)

        movies = cls.get(random_tconst)

        # Keep trying until we find a movie since the id space is not dense.
        if len(movies) == 0:
            return cls.get_random()
        else:
            return movies

    @classmethod
    def find_exact(cls, params, limit):
        params_filtered = cls._filter_search_params(params)

        params_string = ' AND '.join(['{} = :{}'.format(k, k) for k in params_filtered.keys()])
        if params_string:
            params_string = 'WHERE ' + params_string

        query = text("SELECT * FROM movies " + params_string + " LIMIT :limit")
        result = engine.execute(query, **params_filtered, limit=limit)
        return cls._unmarshall_many(result)
    
    @classmethod
    def find_fuzzy(cls, params, limit):
        params_filtered = cls._filter_search_params(params)
        
        params_string = ' AND '.join(['levenshtein({}::varchar(255), (:{})::varchar(255) ) <= 3'.format(k, k) for k in params_filtered.keys()])
        if params_string:
            params_string = 'WHERE ' + params_string
        
        query = text("SELECT * FROM movies " + params_string + " LIMIT :limit")
        result = engine.execute(query, **params_filtered, limit=limit)
        return cls._unmarshall_many(result)

    @classmethod
    def create(cls, params):
        params_filtered = cls._filter_search_params(params, True)

        if len(params_filtered) == 0:
            print('All params filtered from create: %s' % tconst)
            return

        params_string = ', '.join(['{}'.format(k) for k in chain(cls._primary_key, params_filtered.keys())])
        bind_vars_string = ', '.join([':{}'.format(k) for k in chain(cls._primary_key, params_filtered.keys())])

        with engine.begin() as connection:
            # Generate a new, unique primary key by selecting the numeric suffix of the largest known id.
            max_tconst = connection.scalar(text('SELECT SUBSTRING(MAX(tconst), 3) from movies'))
            tconst = 'tt%s' % (int(max_tconst) + 1)

            # Insert the new record
            query = text("INSERT INTO movies (" + params_string + ") VALUES (" + bind_vars_string + ") RETURNING tconst")
            result = connection.execute(query, **params_filtered, tconst=tconst)

            # Return the new record id. NOTE: This only works for single row inserts.
            new_tconst = result.fetchone()[0]

            if tconst != new_tconst:
                print("Unexpected difference in inserted id: %s, %s" % (tconst, new_tconst))

            return new_tconst

    @classmethod
    def update(cls, tconst, params):
        params_filtered = cls._filter_search_params(params, True)

        if len(params_filtered) == 0:
            print('All params filtered from update: %s' % tconst)
            return

        params_string = ', '.join(['{} = :{}'.format(k, k) for k in params_filtered.keys()])

        query = text("UPDATE movies SET " + params_string + " WHERE tconst = :tconst")

        with engine.begin() as connection:
            result = connection.execute(query, **params_filtered, tconst=tconst)

            row_count = result.rowcount

            if row_count != 1:
                print("Unexpected difference in updated row count: %s, %s" % (tconst, row_count))

    @classmethod
    def delete(cls, tconst):
        with engine.begin() as connection:
            result = connection.execute(text("DELETE FROM movies WHERE tconst = :tconst"), tconst=tconst)

            row_count = result.rowcount

            if row_count != 1:
                print("Unexpected difference in deleted row count: %s, %s" % (tconst, row_count))

    @classmethod
    def _filter_search_params(cls, params, filter_immutable_columns=None):
        if filter_immutable_columns is None:
            filter_immutable_columns = False

        params_filtered = {}

        for k, v in params.items():
            if filter_immutable_columns and k in cls._primary_key:
                continue
            if k in cls._column_set and v:
                params_filtered[k] = v

        return params_filtered

    @classmethod
    def _serialize(cls, row):
        return {column: value for column, value in row.items()}

    @classmethod
    def _unmarshall(cls, row):
        kwargs = cls._serialize(row)
        return Movie(**kwargs)

    @classmethod
    def _unmarshall_many(cls, result):
        return [cls._unmarshall(row) for row in result]


class MovieSummary:
    """
    Summary counts of all movies currently in the database.
    """

    _column_set = {'category', 'value'}

    def __init__(self, category, value):
        self.category = category
        # For readability, convert numeric value to comma separated value.
        self.value = '{:,}'.format(value)

    @classmethod
    def movie_summary(cls):
        movie_summaries = []
        movie_summaries.append(cls.count_movies())
        #movie_summaries.append(cls.count_types())
        #movie_summaries.append(cls.count_genres())

        return movie_summaries

    @classmethod
    def count_movies(cls):
        total_count = engine.scalar(text("SELECT COUNT(*) FROM movies"))
        return MovieSummary('Movie Count', total_count)

    # TODO: Expensive query, needs to be placed behind view and/or separate summary table updated via trigger.
    @classmethod
    def count_types(cls):
        total_count = engine.scalar(text("SELECT COUNT(DISTINCT(titletype)) from movies"))
        return MovieSummary('Distinct Movie Types', total_count)

    # TODO: Expensive query, needs to be placed behind view and/or separate summary table updated via trigger.
    @classmethod
    def count_genres(cls):
        total_count = engine.scalar(text("SELECT COUNT(DISTINCT(genres)) from movies"))
        return MovieSummary('Distinct Genres', total_count)

    '''
    @classmethod
    def count_by_decade(cls):
        total_count = engine.scalar(text("SELECT COUNT(*) FROM movies"))
        return MovieSummary('Total Count', total_count)

    @classmethod
    def count_all(cls):
        total_count = engine.scalar(text("SELECT COUNT(*) FROM movies"))
        return MovieSummary('Total Count', total_count)
    '''
