#Import the app object, the flask functions, and the application forms and models
from application import app
from flask import render_template, jsonify, redirect, url_for, request

from .forms import *
from .models import *
from .tables import *

# Enforce query pagination to avoid returning the world.
DEFAULT_QUERY_LIMIT = app.config['DEFAULT_QUERY_LIMIT']

# A redirecting URL that pushes to the movies URL
@app.route('/', methods=["GET"])
def home():
    return redirect(url_for('movies'))

# This function accepts web requests, finding data about movies based on user provided search criteria.
@app.route('/movies', methods=["GET", "POST"])
def movies():
    form = MovieForm(request.form)

    # POST
    if request.method == "POST":
        # Handle create, update, and delete requests.
        if form.create_update_button_click.data == True:
            # Check for update:
            if form.tconst.data:
                tconst = form.tconst.data
                print("Update existing record: %s" % tconst)
                Movie.update(form.tconst.data, form.data)

                movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
                movie_results_table = MovieResultTable(Movie.get(tconst))
                return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)
            else:
                print("Create new record.")
                tconst = Movie.create(form.data)

                movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
                movie_results_table = MovieResultTable(Movie.get(tconst))
                return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)

            movie_results_table = MovieResultTable(Movie.find_exact(form.data, DEFAULT_QUERY_LIMIT))
            return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)

        # Handle user delete requests.
        if form.delete_button_click.data == True:
            if form.tconst.data:
                tconst = form.tconst.data
                print("Delete existing record: %s" % tconst)
                Movie.delete(tconst)

            movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
            movie_results_table = MovieResultTable(Movie.get_all(DEFAULT_QUERY_LIMIT))
            return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)

        # Handle fuzzy search
        if form.fuzzy_search_button_click.data == True:
            print("Fuzzy Search - movie query")
            
            movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
            movie_results_table = MovieResultTable(Movie.find_fuzzy(form.data, DEFAULT_QUERY_LIMIT))
            return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)

        # Handle user search requests.
        if form.random_button_click.data == True:
            # Handle request for a random movie.
            print("Search - random movie")

            movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
            movie_results_table = MovieResultTable(Movie.get_random())
            return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)
        else:
            # Handle a standard user search.
            print("Search - custom movie query")

            movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
            movie_results_table = MovieResultTable(Movie.find_exact(form.data, DEFAULT_QUERY_LIMIT))
            return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)

    # GET - Handle an initial page load.
    print("Search - default movie listing")

    movie_summary_table = MovieSummaryTable(MovieSummary.movie_summary())
    movie_results_table = MovieResultTable(Movie.get_all(DEFAULT_QUERY_LIMIT))
    return render_template('index.html', form=form, movie_summary_table=movie_summary_table, movie_results_table=movie_results_table)
