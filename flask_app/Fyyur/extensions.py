from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from sqlalchemy.orm import DeclarativeBase
from flask_wtf.csrf import CSRFProtect

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
moment = Moment()
csrf = CSRFProtect()