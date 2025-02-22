from django.urls import path
from .views import manager_dashboard, employee_dashboard, create_task, view_task, update_task, delete_task, task_details

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("user-dashboard/", employee_dashboard),
    path("task-form/", create_task, name= "task-form"),
    path("task-details/<int:task_id>/details/", task_details, name='task-details'),
    path("show-task/", view_task),
    path("update-task/<int:id>/", update_task,  name="update-task"),
    path("delete-task/<int:id>/", delete_task,  name="delete-task"),
]
 