from flask import Blueprint

artists_bp = Blueprint(
    "artists",
    __name__,
    template_folder="templates/artists/",
    url_prefix="/artists"
)

from . import routes