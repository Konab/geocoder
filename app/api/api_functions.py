from app import db
from sqlalchemy import func

def get_address_geom(address):
	# Находит геометрию по адрессу
	# Возвращает Geometry
	return db.session.scalar(func.Cos_getaddressgeom(address))

def get_street_geom(building, street):
	# Находит ближайшую дорогу от здания
	# Возвращает Geometry
	return db.session.scalar(func.Cos_getnearstreet(building, street))

def make_point_geom(point):
	# Переводит точку в geom
	# Возвращает Geometry
	return df.session.scalar(func.Cos_makepoint(point))
