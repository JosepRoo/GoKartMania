import os

"""
The following environment variables are suggested to be set.
If the database URLs are not set, the application will default
to a sqlite database stored in the root of the application
directory named data-x.sqlite where x is the current config name.

SECRET_KEY
DEV_DATABASE_URL
PRODUCTION_DATABASE_URL
FLASK_CONFIG (will be development, testing, production or default)
"""

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    STATIC_FOLDER = os.path.join(os.pardir, 'static/dist')
    JWT_SECRET_KEY = SECRET_KEY
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '%Iu4L14pr0J3kT!#%'


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'production': Config
}
