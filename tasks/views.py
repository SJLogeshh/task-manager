from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.utils.timezone import now


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    return render(request, "tasks/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "tasks/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):

    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        category = request.POST.get("category")

        Task.objects.create(
            title=title,
            user=request.user,
            due_date=due_date if due_date else None,
            category=category
        )
        return redirect("home")

    tasks = Task.objects.filter(user=request.user)

    # SEARCH
    query = request.GET.get("q")
    if query:
        tasks = tasks.filter(title__icontains=query)

    # FILTER
    status = request.GET.get("status")
    if status == "completed":
        tasks = tasks.filter(completed=True)
    elif status == "pending":
        tasks = tasks.filter(completed=False)

    # DASHBOARD
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

    return render(request, "tasks/home.html", {
        "tasks": tasks,
        "total": total,
        "completed": completed,
        "pending": pending,
        "today": now().date()
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    # if task.status == 'C':
    #     task.status = 'P'
    # else:
    #     task.status = 'C'

    task.completed = not task.completed
    task.save()

    return redirect("home")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("home")

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)  # ✅ SECURITY FIX

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.category = request.POST.get("category")

        due_date = request.POST.get("due_date")

        # ✅ SAFE DATE HANDLING
        if due_date:
            task.due_date = due_date
        else:
            task.due_date = None

        task.save()
        return redirect("home")

    return render(request, "tasks/edit_task.html", {"task": task})