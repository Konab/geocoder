from app.main import bp


@bp.route("/")
def index():
	name = Super.query.filter_by(id=1).first()
	return "Hello, {}".format(name)
