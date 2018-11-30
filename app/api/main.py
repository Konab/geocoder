from flask import jsonify, request, url_for
from app import db
from app.api import bp
from app.models import Authors
from app.api.errors import bad_request


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
	return jsonify({'connection': 'DONE'})

@bp.route('/get_address_point/<address>', methods=['GET'])
def get_address_point(address):
	response = db.session.scalar(func.Cos_getaddrespoint(address))
	return jsonify(response)


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
