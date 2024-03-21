from flask import render_template
from Fyyur.home import home_bp

@home_bp.route('/')
def index():
    return render_template('home.html')