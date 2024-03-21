from Fyyur.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    genres = db.Column(ARRAY(db.String(120)))
    address = db.Column(db.String(200))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(512))
    facebook_link = db.Column(db.String(512))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)
    image_link = db.Column(db.String(512))
    shows = db.relationship('Show', backref="venue", lazy=True)

    def __repr__(self):
        return f'<Venue "{self.name}">'