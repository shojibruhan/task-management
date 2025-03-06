from django.urls import path
from .views import manager_dashboard, employee_dashboard, dashboard, CreateTask, ViewProject, TaskDetails, UpdatTask, DeleteEvent
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("user-dashboard/", employee_dashboard, name="user-dashboard"),
    path("create-task/", CreateTask.as_view(), name= "create-task"),
    path("task-details/<int:task_id>/details/", TaskDetails.as_view(), name='task-details'),
    path("show-task/", ViewProject.as_view(), name="view-task"),
    path("update-task/<int:id>/", UpdatTask.as_view(),  name="update-task"),
    path("delete-task/<int:id>/", DeleteEvent.as_view(),  name="delete-task"),
    path('dashboard/', dashboard, name='dashboard'),
 
]
 