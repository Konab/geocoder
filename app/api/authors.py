from flask import jsonify
from app.api import bp
from app.models import Authors

@bp.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
	return jsonify(Authors.query.get_or_404(id).to_dict())

@bp.route('/authors', methods=['GET'])
def get_authors():
	pass

@bp.route('/authors', methods=['POST'])
def create_author():
	pass

@bp.route('/authors/<int:id>', methods=['PUT'])
def update_author(id):
	pass
