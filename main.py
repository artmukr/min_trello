from settings import app, api

from views.dashboards import Dashboards
from views.tasks import Tasks, ConcreteTask
from views.users import Users, ConcreteUser

api.add_resource(Dashboards, '/dashboards')

api.add_resource(Tasks, '/dashboards/<int:dashboard_id>')
api.add_resource(ConcreteTask, '/dashboards/<int:dashboard_id>/<int:task_id>')

api.add_resource(Users, '/users')
api.add_resource(ConcreteUser, '/users/<int:user_id>')
# look at query parametrs - need or now

if __name__ == '__main__':
    app.run(debug=True, port=5999)
