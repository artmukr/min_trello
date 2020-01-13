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
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_dashboards = db.relationship(
        'Dashboard', secondary=dashboard_users_table,
        backref=db.backref('dashboards'))

    user_tasks = db.relationship(
        'Task', secondary=task_users_table,
        backref=db.backref('tasks')
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
    members = db.relationship(
        "User", secondary=dashboard_users_table,
        backref="members"
    )
    tasks = db.relationship('Task', backref='tasks')

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    performers = db.relationship(
        'performer', secondary=task_users_table,
        backref='performers'
    )
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title
        }


if __name__ == '__main__':
    db.create_all()
