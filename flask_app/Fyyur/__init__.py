from flask import Flask
from config import Config
from Fyyur.extensions import db, migrate, moment, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # initialize Flask extension here
    db.init_app(app)
    from Fyyur.models import show, artist, venue
    migrate.init_app(app, db)
    moment.init_app(app)
    csrf.init_app(app)

    from Fyyur.home import home_bp
    from Fyyur.artists import artists_bp
    from Fyyur.shows import shows_bp
    from Fyyur.venues import venues_bp
    app.register_blueprint(blueprint=home_bp)
    app.register_blueprint(blueprint=artists_bp)
    app.register_blueprint(blueprint=shows_bp)
    app.register_blueprint(blueprint=venues_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app