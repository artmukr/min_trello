from flask import request
from flask_restful import Resource
from models import User, serialize_multiple, Task
from settings import db
from utils.validator import ModelValidator


class Users(Resource):
	def get(self):
		return serialize_multiple(User.query.all())

	def post(self):
		data = request.get_json()
		user = User(**data)
		db.session.add(user)
		ModelValidator.post_user(user)

		user_id = user.id
		db.session.commit()
		return {"id": user_id}, 201


class ConcreteUser(Resource):
	def get(self, _id):
		User.serialize(User.query.get(_id))

	def delete(self, _id):
		db.session.query(User).filter_by(id=_id).delete()
		db.session.commit()
		return 200


class UserToTask(Resource):
	def post(self, user_id, task_id):
		user = User.query.get(user_id)
		task = Task.query.get(task_id)
		return ModelValidator.validate_user(user, task)
