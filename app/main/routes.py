from app.main import bp
from app.models import Authors
from sqlalchemy import func


@bp.route("/")
def index():
	# name = Authors.query.filter_by(id=1).first().name
	name = db.session.scalar(func(Cos_getaddrespoint('Оренбург Спартаковская 63')))
	return "Hello, {}".format(name)
