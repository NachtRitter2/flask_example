import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap4
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from werkzeug.debug import DebuggedApplication

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bootstrap = Bootstrap4()
moment = Moment()
babel = Babel()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')


# app.debug = True
# app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    if not app.debug and not app.testing:
        if current_app.config['MAIL_SERVER']:
            auth = None
            if current_app.config['MAIL_USERNAME'] or current_app.config['MAIL_PASSWORD']:
                auth = (current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            secure = None
            if current_app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                    mailhost=(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']),
                    fromaddr='no-reply@' + current_app.config['MAIL_SERVER'],
                    toaddrs=current_app.config['ADMINS'], subject='Trakr site failure',
                    credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/trakr.log', maxBytes=10240,
                backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Trakr Startup')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from app import models
