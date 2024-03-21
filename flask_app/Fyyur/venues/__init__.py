from flask import Blueprint


venues_bp = Blueprint(
  "venues", 
  __name__, 
  template_folder="templates/", 
  url_prefix="/venues"
)

from . import routes