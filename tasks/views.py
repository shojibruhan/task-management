from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
        'name': ['C', 'C++', 'Python', 'JavaScript', 'HTML', "CSS", "DJango"],
        "age": 34
    }
    return render(request, 'test.html', context)

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
