#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
from models import db, Artist, Venue, Show
db.init_app(app)

migrate = Migrate(app, db)

# TODO:


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


    # TODO: implement any missing fields, as a database migration using Flask-Migrate



    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.order_by('id').all()
  data = []
  groups = {}

  for venue in venues:
    if (venue.city, venue.state) in groups:
      groups[(venue.city, venue.state)].append(venue)
    else:
      groups[(venue.city, venue.state)] = [venue]
  for group in groups:
    value = {
      "city": group[0],
      "state": group[1],
      "venues": []
    }
    for venue in groups[group]:
      value["venues"].append({
        "id": venue.id,
        "name": venue.name
      })
    data.append(value)
  return render_template('pages/venues.html', areas=data)
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  #data=[{
  #  "city": "San Francisco",
   # "state": "CA",
  #  "venues": [{
  #    "id": 1,
  #    "name": "The Musical Hop",
  #    "num_upcoming_shows": 0,
   # }, {
   #   "id": 3,
  #    "name": "Park Square Live Music & Coffee",
  #    "num_upcoming_shows": 1,
   # }]
 # }, {
  #  "city": "New York",
  #  "state": "NY",
  #  "venues": [{
  #    "id": 2,
   #   "name": "The Dueling Pianos Bar",
   #   "num_upcoming_shows": 0,
   # }]
  #}]
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  keyword = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{keyword}%'))
  response={
  "count": result.count(),
    "data": result
  }
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
   #  "count": 1,
   #  "data": [{
   #    "id": 2,
   #    "name": "The Dueling Pianos Bar",
   #    "num_upcoming_shows": 0,
   #  }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)  
  past_shows = []
  upcoming_shows = []

  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  past_shows_query = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  for show, artist in past_shows_query:
    past_shows.append({
      "artist_id":artist.id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":format_datetime(str(show.start_time)),
    })
    venue.update({
      "past_shows_count": len(past_shows),
    })

  upcoming_shows_query = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()   
  for show, artist in upcoming_shows_query:
    upcoming_shows.append({
      "artist_id":artist.id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":format_datetime(str(show.start_time)),
    })
    venue.update({
      "upcoming_shows_count": len(upcoming_shows),
    })

  #data1={
  #  "id": 1,
  #  "name": "The Musical Hop",
   # "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #  "address": "1015 Folsom Street",
  #  "city": "San Francisco",
  #  "state": "CA",
  #  "phone": "123-123-1234",
  #  "website": "https://www.themusicalhop.com",
  #  "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #  "seeking_talent": True,
  #  "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #  "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #  "past_shows": [{
  #    "artist_id": 4,
  #    "artist_name": "Guns N Petals",
  #    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #    "start_time": "2019-05-21T21:30:00.000Z"
 #   }],
 #   "upcoming_shows": [],
 #   "past_shows_count": 1,
#    "upcoming_shows_count": 0,
 # }
 # data2={
 #   "id": 2,
 #   "name": "The Dueling Pianos Bar",
 #   "genres": ["Classical", "R&B", "Hip-Hop"],
#    "address": "335 Delancey Street",
#    "city": "New York",
 #   "state": "NY",
 #   "phone": "914-003-1132",
 #   "website": "https://www.theduelingpianos.com",
 #   "facebook_link": "https://www.facebook.com/theduelingpianos",
 #   "seeking_talent": False,
 #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
#    "past_shows": [],
#    "upcoming_shows": [],
 #   "past_shows_count": 0,
#    "upcoming_shows_count": 0,
#  }
#  data3={
 #   "id": 3,
 #   "name": "Park Square Live Music & Coffee",
 #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
 #   "address": "34 Whiskey Moore Ave",
 #   "city": "San Francisco",
 #   "state": "CA",
 #   "phone": "415-000-1234",
 #   "website": "https://www.parksquarelivemusicandcoffee.com",
#    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #  "seeking_talent": False,
 #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
 #   "past_shows": [{
#      "artist_id": 5,
 #     "artist_name": "Matt Quevedo",
#      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
 #     "start_time": "2019-06-15T23:00:00.000Z"
 #   }],
 #   "upcoming_shows": [{
 #     "artist_id": 6,
 #     "artist_name": "The Wild Sax Band",
#      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
 #     "start_time": "2035-04-01T20:00:00.000Z"
#    }, {
 #     "artist_id": 6,
#      "artist_name": "The Wild Sax Band",
#      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#      "start_time": "2035-04-08T20:00:00.000Z"
#    }, {
 #     "artist_id": 6,
#      "artist_name": "The Wild Sax Band",
#      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
 #     "start_time": "2035-04-15T20:00:00.000Z"
 #   }],
 #   "past_shows_count": 1,
 #   "upcoming_shows_count": 1,
 # }
 # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate_on_submit():
    try:
      venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data, 
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data,
      website=form.website_link.data
      )
      db.session.add(venue)
      db.session.commit()
    except:
      error = True  
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    if not error:
      flash('Venue ' + request.form['name'] + ' has been successfully listed!')
    else:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')
  else:
    for field, message in form.errors.items():
      flash(field + ' - ' + str(message), 'danger')
  return render_template('forms/new_venue.html', form=form)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = []

  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  keyword = request.form.get('search_term', '')
  result = Artist.query.filter(Artist.name.ilike(f'%{keyword}%'))
  response={
    "count": result.count(),
    "data": result
  }
  # response={
   #  "count": 1,
   #  "data": [{
   #    "id": 4,
   #    "name": "Guns N Petals",
   #    "num_upcoming_shows": 0,
   #  }]
   #}
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  past_shows = []
  upcoming_shows = []

  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_talent": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  past_shows_query = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()   
  for show, venue in past_shows_query:
    past_shows.append({
      "venue_id":venue.id,
      "venue_name":venue.name,
      "venue_image_link":venue.image_link,
      "start_time":format_datetime(str(show.start_time)),
    })
    artist.update({
      "past_shows_count": len(past_shows),
    })

  upcoming_shows_query = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()   
  for show, venue in upcoming_shows_query:
    upcoming_shows.append({
      "venue_id":venue.id,
      "venue_name":venue.name,
      "venue_image_link":venue.image_link,
      "start_time":format_datetime(str(show.start_time)),
    })
    artist.update({
      "upcoming_shows_count": len(upcoming_shows),
    })
  return render_template('pages/show_artist.html', artist=artist)
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  #data1={
  #  "id": 4,
   # "name": "Guns N Petals",
   # "genres": ["Rock n Roll"],
   # "city": "San Francisco",
    #"state": "CA",
    #"phone": "326-123-5000",
    #"website": "https://www.gunsnpetalsband.com",
    #"facebook_link": "https://www.facebook.com/GunsNPetals",
    #"seeking_venue": True,
    #"seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #"image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
   # "past_shows": [{
   #   "venue_id": 1,
   #   "venue_name": "The Musical Hop",
    #  "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
   #   "start_time": "2019-05-21T21:30:00.000Z"
   # }],
   # "upcoming_shows": [],
   # "past_shows_count": 1,
   # "upcoming_shows_count": 0,
 # }
 # data2={
    #"id": 5,
    #"name": "Matt Quevedo",
  #  "genres": ["Jazz"],
    #"city": "New York",
   # "state": "NY",
    #"phone": "300-400-5000",
   # "facebook_link": "https://www.facebook.com/mattquevedo923251523",
   # "seeking_venue": False,
   # "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
   # "past_shows": [{
   #   "venue_id": 3,
  #    "venue_name": "Park Square Live Music & Coffee",
   #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
   #   "start_time": "2019-06-15T23:00:00.000Z"
   # }],
  #  "upcoming_shows": [],
   # "past_shows_count": 1,
  #  "upcoming_shows_count": 0,
 # }
  #data3={
   # "id": 6,
   # "name": "The Wild Sax Band",
   # "genres": ["Jazz", "Classical"],
   # "city": "San Francisco",
    #"state": "CA",
    #"phone": "432-325-5432",
   # "seeking_venue": False,
   # "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #"past_shows": [],
   # "upcoming_shows": [{
   #   "venue_id": 3,
   #   "venue_name": "Park Square Live Music & Coffee",
   #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
   #   "start_time": "2035-04-01T20:00:00.000Z"
   # }, {
   #   "venue_id": 3,
   #   "venue_name": "Park Square Live Music & Coffee",
   #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
   #   "start_time": "2035-04-08T20:00:00.000Z"
   # }, {
  #    "venue_id": 3,
   #   "venue_name": "Park Square Live Music & Coffee",
   #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
   #   "start_time": "2035-04-15T20:00:00.000Z"
  #  }],
   # "past_shows_count": 0,
  #  "upcoming_shows_count": 3,
 # }
 # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data = Artist.query.get(artist_id)
  artist={
    "id": data.id,
    "name": data.name,
    "genres": data.genres,
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website_link": data.website,
    "facebook_link": data.facebook_link,
    "seeking_venue": data.seeking_venue,
    "seeking_description": data.seeking_description,
    "image_link": data.image_link,
  }
  #artist={
  #  "id": 4,
  #  "name": "Guns N Petals",
   # "genres": ["Rock n Roll"],
  #  "city": "San Francisco",
  #  "state": "CA",
  #  "phone": "326-123-5000",
  #  "website": "https://www.gunsnpetalsband.com",
  #  "facebook_link": "https://www.facebook.com/GunsNPetals",
  #  "seeking_venue": True,
  #  "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #  "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  #}
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  try:
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state= form.state.data
    artist.phone= form.phone.data
    artist.genres= form.genres.data
    artist.image_link= form.image_link.data
    artist.facebook_link= form.facebook_link.data
    artist.website= form.website.data
    artist.seeking_venue= form.seeking_venue.data
    artist.seeking_description= form.seeking_description.data
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist has been updated successfully', 'success')
  else:
    flash('Artist could not be updated', 'failure')
  return redirect(url_for('show_artist', artist_id=artist_id))
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  data = Venue.query.get(venue_id)
  venue={
    'id': data.id,
    'name': data.name,
    'genres': data.genres,
    'address': data.address,
    'city': data.city,
    'state': data.state,
    'phone': data.phone,
    'website': data.website,
    'facebook_link': data.facebook_link,
    'seeking_talent': data.seeking_talent,
    'seeking_description': data.seeking_description,
    'image_link': data.image_link
  }
   #venue={
   #  "id": 1,
   #  "name": "The Musical Hop",
    # "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    # "address": "1015 Folsom Street",
   #  "city": "San Francisco",
    # "state": "CA",
   #  "phone": "123-123-1234",
   #  "website": "https://www.themusicalhop.com",
   #  "facebook_link": "https://www.facebook.com/TheMusicalHop",
    # "seeking_talent": True,
   #  "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
   #  "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
   #}
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  form  = VenueForm()
  venue = Venue.query.get(venue_id)
  try:
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state= form.state.data
    venue.address= form.address.data
    venue.phone= form.phone.data
    venue.genres= form.genres.data
    venue.image_link= form.image_link.data
    venue.facebook_link= form.facebook_link.data
    venue.website= form.website.data
    venue.seeking_talent= form.seeking_talent.data
    venue.seeking_description= form.seeking_description.data
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue has been updated successfully', 'success')
  else:
    flash('Venue could not be updated', 'failure')
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate_on_submit():
    try:    
      artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website=form.website_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
      )
      db.session.add(artist)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    if not error:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')
  else:
    for field, message in form.errors.items():
      flash(field + ' - ' + str(message), 'danger')
  return render_template('forms/new_artist.html', form=form)
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.order_by(db.desc(Show.start_time))

  data = []

  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    })
  # displays list of shows at /shows
  # TODO: replace with real venues data.
   #data=[{
   #  "venue_id": 1,
    #  "venue_name": "The Musical Hop",
   #  "artist_id": 4,
    # "artist_name": "Guns N Petals",
   #  "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
   #  "start_time": "2019-05-21T21:30:00.000Z"
   #}, {
  #   "venue_id": 3,
   #  "venue_name": "Park Square Live Music & Coffee",
   #  "artist_id": 5,
   #  "artist_name": "Matt Quevedo",
    #  "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    # "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
   #  "venue_id": 3,
   #  "venue_name": "Park Square Live Music & Coffee",
   #  "artist_id": 6,
   #  "artist_name": "The Wild Sax Band",
   #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    # "start_time": "2035-04-01T20:00:00.000Z"
   #}, {
    # "venue_id": 3,
    # "venue_name": "Park Square Live Music & Coffee",
    # "artist_id": 6,
   #  "artist_name": "The Wild Sax Band",
   #  "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
   #  "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
   #  "venue_id": 3,
   #  "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
   #  "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #  "start_time": "2035-04-15T20:00:00.000Z"
  #}]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False 
  form = ShowForm(request.form)
  try:      
    show = Show(
    artist_id=form.artist_id.data,
    venue_id=form.venue_id.data,
    start_time=form.start_time.data
    )
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  return render_template('pages/home.html')
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
