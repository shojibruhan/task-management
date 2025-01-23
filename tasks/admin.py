from django.contrib import admin
from .models import Employee, Task, TaskDetail, Project


admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(TaskDetail)
admin.site.register(Project)
