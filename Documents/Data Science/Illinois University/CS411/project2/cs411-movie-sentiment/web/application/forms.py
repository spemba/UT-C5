from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, SelectMultipleField, StringField, SubmitField

titletype_array_for_select_field = [
    ('',''),
    ('tvShort','TV Short'),
    ('movie','Movie'),
    ('tvMovie', 'TV Movie'),
    ('short', 'Short'),
    ('tvMiniSeries', 'TV Mini Series'),
    ('videoGame', 'Video Game'),
    ('tvEpisode', 'TV Episode'),
    ('video', 'Video'),
    ('tvSpecial', 'TV Special'),
    ('tvSeries', 'TV Series')
]

isadult_array_for_select_field = [
    ('', ''),
    ('0', 'No'),
    ('1', 'Yes')
]

class MovieForm(FlaskForm):
    tconst = StringField('Id')
    titletype = SelectField('Type', choices=titletype_array_for_select_field, default='')
    primarytitle = StringField('Primary Title')
    originaltitle = StringField('Original Title')
    isadult = SelectField('Is Adult', choices=isadult_array_for_select_field, default='')
    startyear = IntegerField('Start Year')
    endyear = IntegerField('End Year')
    runtimeminutes = IntegerField('Run Time In Minutes')
    genres = StringField('Genres')

    create_update_button_click = SubmitField('Create/Update Movie')
    delete_button_click = SubmitField('Delete Movie')

    search_button_click = SubmitField('Search for Movies')
    fuzzy_search_button_click = SubmitField('Fuzzy Search for Movies')
    random_button_click = SubmitField('Pick a Random Movie!')
