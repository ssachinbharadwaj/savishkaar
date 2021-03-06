from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from .models import departments
# Create your views here.


def home(request):
    return render(request, "home.html")

def signupuser(request):
    if request.method == 'GET':
        return render(request, "signupuser.html", {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('currenttodo')
            except IntegrityError: 
                return render(request, "signupuser.html", {'form': UserCreationForm(), 'error':'Username has already been taken please choose new username'})   
        else:
            return render(request, "signupuser.html", {'form': UserCreationForm(), 'error':'passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, "loginuser.html", {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request, "loginuser.html", {'form': AuthenticationForm(), 'error': 'Username and Password did not match'})   
        else:
            login(request, user)
            return redirect('currenttodo')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createtodo(request):
    if request.method == 'GET':
        return render(request, "createtodo.html", {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, "createtodo.html", {'form': TodoForm(), 'error': 'Bad data passed in'})  

def currenttodo(request):
    err_msg = ""

    if request.method == 'POST':
        depts = departments()
        depts.name =  request.POST['department']
        try:
            depts.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                err_msg = "Department already exists"
    
    dep_list = departments.objects.all()
    for dep in dep_list:
        print(dep.name)
    return render(request, 'currenttodo.html', {'dep_list': dep_list, 'error': err_msg})