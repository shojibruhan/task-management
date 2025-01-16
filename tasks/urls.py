from django.urls import path
from .views import show_task

urlpatterns = [
    path("show-task/", show_task)
]
