from flask import request
from flask_restful import Resource
from models import Task, serialize_multiple
from utils.validator import ModelValidator
from settings import db


class Tasks(Resource):
	def get(self, dashboard_id):
		return serialize_multiple(Task.query.filter_by(
			dashboard_id=dashboard_id)), 201

	def post(self, dashboard_id):
		data = request.get_json()
		task = Task(**data, dashboard_id=dashboard_id)
		if task.status == "to_do" or task.status == "in_progress" or \
			task.status == "done":
			db.session.add(task)
			ModelValidator.post_task(task)

			task_id = task.id
			db.session.commit()
			return {"id": task_id}, 201
		else:
			return "invalid status", 404


class ConcreteTask(Resource):
	def get(self, dashboard_id, task_id):
		return Task.serialize(Task.query.filter_by(
			id=task_id, dashboard_id=dashboard_id)), 204

	def patch(self, dashboard_id, task_id):
		data = request.get_json()
		return ModelValidator(Task).patch_by_task_id_and_dashboard_id(
			dashboard_id, task_id, data)


class Comments(Resource):
	def get(self, task_id):
		return Task.serialize(Task.query.get(task_id))

	def patch(self, task_id):
		data = request.get_json()
		return ModelValidator.patch_by_id(self, task_id, data)


class ChangeStatus(Resource):
	def patch(self, dashboard_id, task_id):
		status = request.args.get('status')
		return ModelValidator.validate_status(dashboard_id, task_id, status)
