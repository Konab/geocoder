from app import db


class Authors(db.Models):
	id = db.Column(db.Ineger, primary_key=True)
	name = db.Column(db.String(120), index=True)
