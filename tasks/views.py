from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Sum, Avg
from django.contrib import messages

def manager_dashboard(request):
    
    
    
    # Getting task count
    # total_task= tasks.count()
    # completed_task= Task.objects.filter(status= "COMPLETED").count()
    # in_progress_task= Task.objects.filter(status= "IN_PROGRESS").count()
    # pending_task= Task.objects.filter(status= "PENDING").count()
    
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


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")



def create_task(request):
    employee= Employee.objects.all( )
    task_form= TaskModelForm() # for 'GET'
    task_detail_form= TaskDetailModelForm()

    
    if request.method== "POST":
        task_form= TaskModelForm(request.POST)
        task_detail_form= TaskDetailModelForm(request.POST)
        
        if task_form.is_valid() and task_detail_form.is_valid():

            """     or Model Form Data    """
            # print(form)
            task= task_form.save()
            task_detail= task_detail_form.save(commit=False)
            task_detail.task= task
            task_detail.save()

            messages.success(request, "Task added Successfully")
            return redirect("task-form")
            
            '''   For Django Form Data   '''
            # data= form.cleaned_data
            # title= data.get('title')
            # description= data.get('description')
            # due_date= data.get('due_date')
            # assigned_to= data.get('assigned_to')

            # task= Task.objects.create(title=title, description=description, due_date= due_date)
             
            # #  assigned employee to task
            # for emp_id in assigned_to:
            #     employee= Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse("Task added Successfully!!!")
            

    context= {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

def view_task(request):
    # tasks= TaskDetail.objects.exclude(priority= 'L')
    # tasks= Task.objects.filter(due_date= date.today())
    # tasks= Task.objects.filter(title__icontains= 'c', status= 'PENDING')
    # tasks= Task.objects.filter(Q(status= 'PENDING') | Q(status= 'IN_PROGRESS'))
    # tasks= Task.objects.all()

    # ||||--------  select_related(foreign_key, OneToOneField)  --------|||||

    # tasks= Task.objects.select_related('details').all()
    # tasks= Task.objects.select_related('project').all()
    # tasks= TaskDetail.objects.select_related('task').all()


    # ||||--------  prefetch_related(reverse_foreign_key, ManyToMany)  --------|||||

    # tasks= Task.objects.prefetch_related('task_set').all()
    # tasks= Project.objects.prefetch_related('task_set').all()
    # tasks= Task.objects.prefetch_related('assigned_to').all()

        
    # Aggregation

    # task_count= Task.objects.aggregate(total= Count('id'))

    # Annotate

    projects= Project.objects.annotate(total_task= Count("task")).order_by('total_task')
    
    return render(request, "show_task.html", {"projects": projects})


