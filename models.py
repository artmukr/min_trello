from __future__ import annotations
from settings import db

dashboard_users_table = db.Table(
    "dashboard_users", db.Model.metadata,
    db.Column('dashboard_id', db.Integer, db.ForeignKey("dashboard.id")),
    db.Column('user_id', db.Integer, db.ForeignKey("user.id"))
)

task_users_table = db.Table(
    'task_users', db.Model.metadata,
    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
              primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    dashboard = db.relationship('Dashboard', backref='creator')
    user_dashboards = db.relationship(
        'Dashboard', secondary=dashboard_users_table,
        primaryjoin=id == dashboard_users_table.c.user_id,
        backref=db.backref('dashboards', lazy='dynamic'))

    user_tasks = db.relationship(
        'Task', secondary=task_users_table,
        primaryjoin=id == task_users_table.c.user_id,
        backref=db.backref('tasks', lazy='dynamic')
    )

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }


class Dashboard(db.Model):
    __tablename__ = 'dashboard'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Task', backref='dashboard')

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


def serialize_multiple_filtered(objects: list, dashboard_id: int):
    users_id_list = [el[1] for el in db.session.query(
        dashboard_users_table).filter_by(dashboard_id=dashboard_id).all()]
    return [User.query.filter_by(
        id=users_id_list[index]).first().serialize()
            for index in range(len(users_id_list))]


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))
    task_users = db.relationship(
        'User', secondary=task_users_table,
        primaryjoin=id == task_users_table.c.task_id,
        backref=db.backref('users', lazy='dynamic')
    )

    status = db.Column(db.String(11), nullable=False)
    comments = db.Column(db.String(1000))

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "comments": self.comments
        }


if __name__ == '__main__':
    db.create_all()
