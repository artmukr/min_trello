from sqlalchemy.exc import InvalidRequestError, IntegrityError
from settings import db


class ModelValidator:
	def __init__(self, model):
		self.model = model

	def get_by_id(self, model_id):
		try:
			return self.model.query.get(model_id).serialize()
		except AttributeError:
			return "Not found", 404

	def patch_by_id(self, model_id, data):
		try:
			db.session.query(self.model).filter_by(id=model_id).update(data)
		except InvalidRequestError:
			return {}, 400
		db.session.commit()
		return {}, 204

	def patch_by_task_id_and_dashboard_id(self, dashboard_id, task_id, data):
		try:
			db.session.query(self.model).filter_by(
				id=task_id, dashboard_id=dashboard_id).update(data)
		except InvalidRequestError:
			return {}, 400
		db.session.commit()
		return {}, 204

	@staticmethod
	def post_user(self):
		try:
			db.session.flush()
		except IntegrityError:
			return 'User already exist', 409
