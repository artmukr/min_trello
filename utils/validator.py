from sqlalchemy.exc import InvalidRequestError, IntegrityError
from settings import db
from models import Task


class ModelValidator:
	def __init__(self, model):
		self.model = model

	def patch_by_id(self, task_id, data):
		try:
			db.session.query(self.model).filter_by(id=task_id).update(data)
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

	@staticmethod
	def post_task(self):
		try:
			db.session.flush()
		except IntegrityError:
			return 'Task already exist', 409

	@staticmethod
	def validate_user(user, task):
		if user.user_dashboards[0].id == task.dashboard_id:
			task.tasks.append(user)
			db.session.commit()
			return {}, 201
		else:
			return 'user does not belong to this dashboard', 409

	@staticmethod
	def validate_status(dashboard_id, task_id, status):
		if status == 'to_do' or status == 'in_progress' or status == 'done':
			db.session.query(Task).filter_by(dashboard_id=dashboard_id,
			                                 id=task_id).update(
				{'status': status})
			return 'status updated', 201
		else:
			return InvalidRequestError, 400
