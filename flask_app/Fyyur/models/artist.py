from Fyyur.extensions import db
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import ARRAY


class Artist(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(120))
    genres: Mapped[list[str]] = db.Column(ARRAY(db.String(120)))
    city: Mapped[str] = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(512))
    facebook_link = db.Column(db.String(512))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)
    image_link = db.Column(db.String(512))
    shows = db.relationship('Show', backref="artist", lazy=True)

    def __repr__(self):
        return f'<Artist "{self.name}">'