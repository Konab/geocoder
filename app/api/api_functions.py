from app import db
from sqlalchemy import func

def get_address_geom(address):
	return db.session.scalar(func.Cos_getaddressgeom(address))

def get_street_geom(street):
	# return 
	pass
