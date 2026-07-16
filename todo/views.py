from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.urls import reverse


# Create your views here.


def index(request):
    if request.method == 'POST':
        raw_due = request.POST.get('due_at', '')
        due = None
        if raw_due:
            due = make_aware(parse_datetime(raw_due))
        description = request.POST.get('description', '')
        task = Task(title=request.POST.get('title', ''), due_at=due, description=description)
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request. POST['title']
        raw_due = request.POST.get('due_at', '')
        if raw_due:
            task.due_at = make_aware(parse_datetime(raw_due))
        else:
            task.due_at = None
        task.description = request.POST.get('description', '')
        task.save()
        return redirect(detail, task_id)
    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task dose not exist")
    task.delete()
    return redirect(index)
