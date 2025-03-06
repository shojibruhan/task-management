from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Task, TaskDetail, Project
from datetime import date, timedelta
from django.db.models import Q, Count, Max, Min, Sum, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy



    

def is_manager(user):
    return user.groups.filter(name= 'Manager').exists()


def is_employee(user):
    return user.groups.filter(name= 'Employee').exists()


@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
   
    counts= Task.objects.aggregate(
        total_task= Count('id'),
        completed_task= Count('id', filter=Q(status= "COMPLETED")),
        in_progress_task= Count('id', filter=Q(status= "IN_PROGRESS")),
        pending_task= Count('id', filter=Q(status= "PENDING"))
    )

    # Retriving task data 
    base_query= Task.objects.select_related('details').prefetch_related('assigned_to')
    type= request.GET.get('type', 'all')
    if type == 'completed':
        tasks= base_query.filter(status= "COMPLETED")
    elif type == 'in_progress':
        tasks= base_query.filter(status= "IN_PROGRESS")
    elif type == 'pending':
        tasks= base_query.filter(status= "PENDING")
    elif type == 'all':
        tasks= base_query.all()

    context= {
        "tasks": tasks,
        "counts": counts
    }
    return render(request, "dashboard/manager-dashboard.html", context)

@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")



create_task_decorators= [login_required, permission_required("tasks.add_task", login_url='no-permission')]

class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name= "task_form.html"
    permission_required= 'tasks.add_task'
    login_url= 'sign-in'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("get_context: ", context)
        context["task_form"] = kwargs.get("task_form", TaskModelForm())
        context["task_detail_form"]= kwargs.get("task_detail_form", TaskDetailModelForm())
        return context
    

    
    def get(self, request, *args, **kwargs):
       
        
        
        context= self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form= TaskModelForm(request.POST)
        task_detail_form= TaskDetailModelForm(request.POST, request.FILES)
        
        if task_form.is_valid() and task_detail_form.is_valid():

            """     or Model Form Data    """
            # print(form)
            task= task_form.save()
            task_detail= task_detail_form.save(commit=False)
            task_detail.task= task
            task_detail.save()

            messages.success(request, "Task added Successfully")
            context= self.get_context_data(task_form= task_form, task_detail_form= task_detail_form)
            return render(request, self.template_name, context)

  





class UpdatTask(UpdateView):
    model= Task
    template_name='task_form.html'
    form_class= TaskModelForm
    context_object_name= 'task'
    pk_url_kwarg= 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form']= self.get_form()
        task= self.get_object()

        if hasattr(self.object, 'details') and  self.object.details:
            context["task_detail_form"] = TaskDetailModelForm(instance= self.object.details)
        else:
            context["task_detail_form"] = TaskDetailModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object= self.get_object()
        task_form= TaskModelForm(request.POST, instance= self.object)
        task_detail_form= TaskDetailModelForm(request.POST, request.FILES, instance= getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """    For Model Form Data    """
            
            task= task_form.save()
            task_detail= task_detail_form.save(commit=False)
            task_detail.task= task
            task_detail.save()

            messages.success(request, "Task updated Successfully")
            return redirect("update-task", self.object.id)
        return redirect('update-tast', self.object.id)
    

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def view_task(request):
    

    projects= Project.objects.annotate(total_task= Count("task")).order_by('total_task')
    
    return render(request, "show_task.html", {"projects": projects})


view_project_decorators= [login_required, permission_required("projects.view_project", login_url='no-permission')]
@method_decorator(decorator=view_project_decorators, name="dispatch")
class ViewProject(ListView):
    model= Project
    context_object_name= 'projects'
    template_name= "show_task.html"

    def get_queryset(self):
        queryset= Project.objects.annotate(total_task= Count("task")).order_by('total_task')
        return queryset
    
    


delete_event_decorator=[login_required, permission_required('tasks.delete_task', login_url='no-permission')]
@method_decorator(delete_event_decorator, name='dispatch')
class DeleteEvent(DeleteView):
    model= Task
    pk_url_kwarg= 'id'
    success_url = reverse_lazy("manager-dashboard")

    def post(self, request, *args, **kwargs):
        self.object= self.get_object()
        self.object.delete()

        messages.success(request, "Event Deleted Successfully !!!")
        return redirect("manager-dashboard")



task_details_decorators= [login_required, permission_required("tasks.view_task", login_url='no-permission')]
@method_decorator(decorator=task_details_decorators, name="dispatch")
class TaskDetails(DetailView):
    model= Task
    template_name= "task_details.html"
    context_object_name= 'task'
    pk_url_kwarg= 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task= self.get_object()
        select_status= request.POST.get('task_status')
        task.status= select_status
        task.save()

        return redirect("task-details", task.id)

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('sign-in')