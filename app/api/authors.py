from flask import jsonify, request
from app.api import bp
from app.models import Authors

@bp.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
	return jsonify(Authors.query.get_or_404(id).to_dict())

@bp.route('/authors', methods=['GET'])
def get_authors():
	page = request.args.get('page', 1, type=int)
	per_page = min(request.args.get('per_page', 10, type=int), 100)
	data = Authors.to_collection_dict(Authors.query, page, per_page, 'api.get_authors')
	return jsonify(data)

@bp.route('/authors', methods=['POST'])
def create_author():
	pass

@bp.route('/authors/<int:id>', methods=['PUT'])
def update_author(id):
	pass
