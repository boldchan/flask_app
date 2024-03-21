from flask import Blueprint

shows_bp = Blueprint(
    "shows",
    __name__,
    template_folder="templates/shows/", 
    url_prefix="/shows"
)

from . import routes