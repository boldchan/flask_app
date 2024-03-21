from collections import defaultdict
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from Fyyur import db
from Fyyur.models import Venue
from Fyyur.venues import venues_bp
from Fyyur.venues.form import VenueForm


@venues_bp.route('/')
def venues():

    all_venues = db.session.scalars(db.select(Venue)).all()
    venues_d = defaultdict(list)
    for venue in all_venues:
        num_upcoming_shows = len(
            [show for show in venue.shows if show.start_time > datetime.today()])
        venues_d[(venue.city, venue.state)].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })
    data = [
        {
            "city": city, 
            "state": state, 
            "venues": venues_d[(city, state)]
        } for city, state in venues_d
    ]
    return render_template('venues/venues.html', areas=data)


@venues_bp.route('/search', methods=['POST'])
def search_venues():
    search_term=request.form.get('search_term', '')
    venues = db.session.scalars(db.select(Venue).where(Venue.name.contains(search_term))).all()
    response = {
        "count": len(venues),
        "data": [
            {
                "id": venue.id, 
                "name": venue.name, 
                "num_upcoming_shows": len([
                    show for show in venue.shows if show.start_time > datetime.today()
                ])
            } for venue in venues
        ]
    }
    return render_template('venues/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@venues_bp.route('/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = db.session.scalars(db.select(Venue).where(Venue.id==venue_id)).first()
    past_shows = [
                {
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                } for show in venue.shows if show.start_time < datetime.today()
            ]
    upcoming_shows = [
                {
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                } for show in venue.shows if show.start_time > datetime.today()
            ]
    data = {
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
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows)
        }

    return render_template('venues/show_venue.html', venue=data)


@venues_bp.route('/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('venues/new_venue.html', form=form)


@venues_bp.route('/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm()
    print(form.name.data)
    
    if form.is_submitted():
        print("submitted")
        print(form.name.data)

    if form.validate_on_submit():
        print("nnn")
        venue = Venue(
            name=form.name.data,
            genres=form.genres.data,
            address=form.address.data,
            city=form.city.data,
            state=form.name.data,
            phone=form.phone.data,
            website=form.website_link.data,
            facebook_link=form.facebook_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data,
            image_link=form.image_link.data
        )
        db.session.add(venue)
        try:
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('venues/venues.html'))
        except:
            db.session.rollback()
            flash(f'An error occurred. {form.errors}')
            return render_template('home.html')


@venues_bp.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = db.session.scalars(db.select(Venue).where(Venue.id==venue_id)).first()
        db.session.delete(venue)
        flash(f'Venue {venue_id} is deleted' )
        return render_template('home.html')
    except:
        db.session.rollback()
        flash(f"An error occured when deleting venue {venue_id}")

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@venues_bp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = db.session.scalars(db.select(Venue).where(Venue.id==venue_id)).first()
    venue_d = {
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
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }
    form = VenueForm(**venue_d)

    return render_template('venues/edit_venue.html', form=form, venue=venue)


@venues_bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = db.session.scalars(db.select(Venue).where(Venue.id==request.form["id"])).first()
    print(venue)
    venue.name = request.form["name"]
    venue.genres = request.form["genres"]
    venue.address = request.form["address"]
    venue.city = request.form["city"]
    venue.state = request.form["state"]
    venue.phone = request.form["phone"]
    venue.website = request.form["website"]
    venue.facebook_link = request.form["facebook_link"]
    venue.seeking_talent = request.form["seeking_talent"]
    venue.seeking_description = request.form["seeking_description"]
    venue.image_link = request.form["image_link"]
    print(venue)

    db.session.commit()
    print("i'm here")
    return redirect(url_for('show_venue', venue_id=venue_id))
