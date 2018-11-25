from app.main import bp
from app.models import Authors


@bp.route("/")
def index():
	name = Authors.query.filter_by(id=1).first()
	return "Hello, {}".format(name)
