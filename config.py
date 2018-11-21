import os

class Config(object):
	SECRET_KEY = os.environ.get('APP_SECRET_KEY') or ''
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or ''
	SQLALCHEMY_TRACK_MODIFICATIONS = False
