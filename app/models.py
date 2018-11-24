from app import db
from flask import url_for


class PaginatedAPIMixin(object):
	@staticmethod
	def to_collection_dict(query, page, per_page, endpoint, **kwargs):
		resources = query.paginate(page, per_page, False)
		data = {
			'items': [item.to_dict() for item in resources.items],
			'_meta': {
				'page': page,
				'per_page': per_page,
				'total_pages': resources.pages,
				'total_items': resources.total
			},
			'_links': {
				'self': url_for(endpoint, page=page, per_page=per_page,
								**kwargs),
				'next': url_for(endpoint, page=page + 1, per_page=per_page,
								**kwargs) if resources.has_next else None,
				'prev': url_for(endpoint, page=page - 1, per_page=per_page,
								**kwargs) if resources.has_prev else None
			}
		}
		return data


class Authors(PaginatedAPIMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), index=True)

	def to_dict(self, include_email=False):
		data = {
			'id': self.id,
			'name': self.name,
			'_links': {
				'self': url_for('api.get_author', id=self.id)
			}
		}
		if include_email:
			data['email'] = self.email
		return data

	def from_dict(self, data, new_user=False):
		for field in ['name']:
			if field in data:
				setattr(self, field, data[field])

