import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or ''
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or ''
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# MAIL_SERVER = os.environ.get('MAIL_SERVER')
	# MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
