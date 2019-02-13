from flask import jsonify, request, url_for
from sqlalchemy import func
from app import db
from app.api import bp
from app.api import api_functions as api_func
from app.models import Authors
from app.api.errors import bad_request
import geocoder


### Get functions
@bp.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
	return jsonify(Authors.query.get_or_404(id).to_dict())

@bp.route('/authors', methods=['GET'])
def get_authors():
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('per_page', 10, type=int), 100)
	data = Authors.to_collection_dict(Authors.query, page, per_page, 'api.get_authors')
	return jsonify(data)

@bp.route('/test', methods=['GET'])
def test_get():
	test = request.args.to_dict()
	return jsonify({'connection': 'DONE', **test})

#######___MAIN_FUNCTION___#######
@bp.route('/get_address_point', methods=['GET'])
def get_address_point():
	'''Выдает геоточку по адресу
	
	Decorators:
		bp.route - общается по .../api/get_address_point

	Arguments:
		address {str} -- адрес на кириллице
	
	Returns:
		json/binary -- словарь с геоданными о здании
	'''
	req = request.args.to_dict()
	address = req['address']
	try:
		response = db.session.scalar(func.Cos_getaddpoint(address)).replace('(', '').replace(')','').split(',')
	except:
		response = geocoder.yandex(address)
		print(address)
		print(response)
	result = dict(zip(('id', 'lat', 'lon'), (response[0], response[1], response[2])))
	return jsonify(result)

@bp.route('/distance')
def get_distance():
	'''Растояние между точками в метрах

	lon и lat идут в таком порядке, для увеличения точности вычислений на стороне PSQL
	
	Decorators:
		bp.route - общается по .../api/distance

	Arguments:
		point_1 {str} -- геоточка в формате Point(lon, lat)
		point_2 {str} -- геоточка в формате Point(lon, lat)
	
	Returns:
		[json/binary] -- словарь с растоянием между точками в метрах и bool входит ли оно в диапазон
	'''
	req = request.args.to_dict()
	response = db.session.scalar(func.Cos_diapason(req['point_1'], req['point_2']))
	result = {'distance': response}
	result['InRange'] = True if response < 300 else False
	return jsonify(result)


@bp.route('/closest_point_on_road')
def get_closest_point_on_road():
	'''Находит проекуию точки на дороге

	Decorators:
		bp.route - общяется по /closest_point_on_road
	
	Returns:
		[json/binary] -- словарь с широтой и долготой искомой точки
	'''
	req = request.args.to_dict()
	address_geom = api_func.get_address_geom(req['address'])
	road_geom = api_func.get_street_geom(address_geom, req['road'])
	response = eval(db.session.scalar(func.Cos_getclosestpoint(address_geom, road_geom)))
	result = {'lat': response[0], 'lon': response[1]}
	return jsonify(result)

@bp.route('/correct_point')
def correct_point():
	req = request.args.to_dict()
	address_geom = api_func.get_address_geom(req['address'])
	road_geom = api_func.get_street_geom(address_geom, req['road'])
	point_geom = api_func.make_point_geom(req['point'])
	if db.session.scalar(func.Cos_diapason_for_geom(address_geom, point_geom)) < 300:
		# Если точка входит в радиус допустимости
		# Находим проекцию точки на дороге для адреса
		closest_address_point = eval(db.session.scalar(func.Cos_getclosestpoint(address_geom, road_geom)))
		# Находим проекцию точки дтп на дороге
		closest_point = eval(db.session.scalar(func.Cos_getclosestpoint(point_geom, road_geom)))
		# Находим среднее между точками
		calculated_point = ((closest_address_point[0]+closest_point[0])/2, (closest_address_point[1]+closest_point[1])/2)
		calculated_point_geom = db.session.scalar(func.cos_makegeom(calculated_point[1], calculated_point[0]))
		reult_point = eval(db.session.scalar(func.Cos_getclosestpoint(calculated_point_geom, road_geom)))
	else:
		reult_point = eval(db.session.scalar(func.Cos_getclosestpoint(address_geom, road_geom)))
	return jsonify({'result': reult_point})


### POST functions
@bp.route('/authors', methods=['POST'])
def create_author():
	data = request.get_json() or {}
	if 'name' not in data:
		return bad_request('must include name field')
	if Authors.query.filter_by(name=data['name']).first():
		return bad_request('please use a different name')
	author = Authors()
	author.from_dict(data, new_user=True)
	db.session.add(author)
	db.session.commit()
	response = jsonify(author.to_dict())
	response.status_code = 201
	response.headers['Location'] = url_for('api.get_author', id=author.id)
	return response

### PUT functions
@bp.route('/authors/<int:id>', methods=['PUT'])
def update_author(id):
	author = Authors.query.get_or_404(id)
	data = request.get_json() or {}
	author.from_dict(data)
	db.session.commit()
	return jsonify(author.to_dict())
