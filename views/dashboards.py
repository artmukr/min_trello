from flask_restful import Resource
from models import Dashboard, serialize_multiple, dashboard_users_table, \
	User, serialize_multiple_filtered
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

		dashboard_id = dashboard.id
		db.session.commit()

		return {"id": dashboard_id}, 201


class UserToDashboard(Resource):
	def post(self, dashboard_id, user_id):
		dashboard = Dashboard.query.get(dashboard_id)
		user = User.query.get(user_id)
		dashboard.dashboards.append(user)
		db.session.commit()
		return {'dashboard_id': dashboard_id, 'user_id': user_id}, 201


class DashboardUsers(Resource):
	def get(self, dashboard_id):
		return serialize_multiple_filtered(User.query.all(), dashboard_id), 201
