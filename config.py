import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yabba-dabba-doo'
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'db/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
