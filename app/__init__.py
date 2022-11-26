from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app.debug = True
# app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
