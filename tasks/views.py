from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Sum, Avg

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")



def create_task(request):
    employee= Employee.objects.all( )
    form= TaskModelForm() # for 'GET'
    
    if request.method== "POST":
        form= TaskModelForm(request.POST)
        if form.is_valid():

            """     or Model Form Data    """
            print(form)
            form.save()
            return render(request, 'task_form.html', {'form': form, "message": "Task added Successfully"})
            
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
            

    context= {"form": form}
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


