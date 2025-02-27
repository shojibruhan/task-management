from django.urls import path
from .views import manager_dashboard, employee_dashboard, create_task, view_task, update_task, delete_task, task_details, dashboard, CreateTask, ViewProject, TaskDetails, UpdatTask
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("user-dashboard/", employee_dashboard, name="user-dashboard"),
    # path("sign-in/", LoginView.as_view(), name="sign-in"),
    # path("create-task/", create_task, name= "create-task"),
    path("create-task/", CreateTask.as_view(), name= "create-task"),
    # path("task-details/<int:task_id>/details/", task_details, name='task-details'),
    path("task-details/<int:task_id>/details/", TaskDetails.as_view(), name='task-details'),
    # path("show-task/", view_task, name="view-task"),
    path("show-task/", ViewProject.as_view(), name="view-task"),
    # path("update-task/<int:id>/", update_task,  name="update-task"),
    path("update-task/<int:id>/", UpdatTask.as_view(),  name="update-task"),
    path("delete-task/<int:id>/", delete_task,  name="delete-task"),
    path('dashboard/', dashboard, name='dashboard'),
 
]
 