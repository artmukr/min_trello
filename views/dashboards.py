from flask_restful import Resource
from models import Dashboard, serialize_multiple
from settings import db
from flask import request


class Dashboards(Resource):
	def get(self):
		return serialize_multiple(Dashboard.query.all())

	def post(self):
		data = request.get_json()

		dashboard = Dashboard(**data)
		db.session.add(dashboard)
		db.session.flush()

		room_id = dashboard.id
		db.session.commit()

		return {"id": room_id}, 201
