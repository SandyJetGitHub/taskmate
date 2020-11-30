from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from todolist_app.models import TaskList
from todolist_app.forms import TaskForms
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    context = {
        'welcome_text':"Welcome to Taskmate",
    }
    return render(request, 'index.html', context)

@login_required
def todo(request):
    if request.method == "POST":
        form = TaskForms(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request, ('New Task Added Successfully!'))
        return redirect('todo')
    else:
        all_task = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(all_task, 5)
        page = request.GET.get('pg')
        all_task = paginator.get_page(page)
        return render(request, 'todo.html', {'all_task':all_task})

def contact(request):
    context = {
        'welcome_text':"Welcome to Contact",
    }
    return render(request, 'contact.html', context)

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ('Access Denied!'))   
    return redirect('todo')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForms(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ('Task Edited Successfully!'))
        return redirect('todo')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj':task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ('Access Denied!'))
    return redirect('todo')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todo')