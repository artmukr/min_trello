from flask import request
from flask_restful import Resource
from models import Task, serialize_multiple
from utils.validator import ModelValidator


class Tasks(Resource):
	def get(self):
		return serialize_multiple(Tasks.query.all()), 201


class ConcreteTask(Resource):
	def get(self, dashboard_id, task_id):
		return Task.serialize(Task.query.filter_by(
			id=task_id, dashboard_id=dashboard_id)), 204

	def patch(self, dashboard_id, task_id):
		data = request.get_json()
		return ModelValidator(Task).patch_by_task_id_and_dashboard_id(
			dashboard_id, task_id, data)
