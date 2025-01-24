from django.urls import path
from .views import manager_dashboard, user_dashboard, create_task, view_task, update_task, delete_task

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("user-dashboard/", user_dashboard),
    path("task-form/", create_task, name= "task-form"),
    path("show-task/", view_task),
    path("update-task/<int:id>/", update_task,  name="update-task"),
    path("delete-task/<int:id>/", delete_task,  name="delete-task")
]
 