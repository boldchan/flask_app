from flask import Blueprint

home_bp = Blueprint(
    'home', 
    __name__, 
    template_folder="templates/homes/"
)

from Fyyur.home import routes

