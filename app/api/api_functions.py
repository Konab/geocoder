from app import db
from sqlalchemy import func

def get_address_geom(address):
	# Возвращает Geometry
	return db.session.scalar(func.Cos_getaddressgeom(address))

def get_street_geom(building, street):
	# Возвращает Geometry
	return db.session.scalar(func.Cos_getnearstreet(building, street))
