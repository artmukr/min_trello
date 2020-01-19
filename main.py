from settings import app, api

from views.dashboards import Dashboards, UserToDashboard, DashboardUsers
from views.tasks import Tasks, ConcreteTask, Comments, ChangeStatus
from views.users import Users, ConcreteUser, UserToTask

api.add_resource(Dashboards,
                 '/dashboards')

api.add_resource(Tasks,
                 '/dashboards/<int:dashboard_id>')

api.add_resource(ConcreteTask,
                 '/dashboards/<int:dashboard_id>/tasks/<int:task_id>')

api.add_resource(Users,
                 '/users')

api.add_resource(ConcreteUser,
                 '/users/<int:user_id>')

api.add_resource(UserToDashboard,
                 '/dashboards/<int:dashboard_id>/users/<int:user_id>')

api.add_resource(DashboardUsers,
                 '/dashboards/<int:dashboard_id>/users')

api.add_resource(UserToTask,
                 '/users/<int:user_id>/tasks/<int:task_id>')

api.add_resource(Comments,
                 '/tasks/<int:task_id>/comments')

api.add_resource(ChangeStatus,
                 '/dashboards/<int:dashboard_id>/tasks/<int:task_id>/status')

if __name__ == '__main__':
    app.run(debug=True, port=5999)
