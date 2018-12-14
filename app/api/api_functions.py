from app import db
from sqlalchemy import func

def get_address_geom(address):
	return response = db.session.scalar(func.Cos_getaddressgeom(address))
