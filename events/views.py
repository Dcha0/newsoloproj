from django.shortcuts import render, redirect
import bcrypt
from time import localtime, strftime
from django.contrib import messages
from .models import *

# Create your views here.
def login(request):
    return render(request, 'login.html')



def loggingIn(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        existing_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), existing_user.password.encode()):
            request.session['user'] = existing_user.fname
            request.session['id'] = existing_user.id
            return redirect('/dashboard')
    messages.error(request, "Username / Password is invalid")
    return redirect("/")



def registration(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(8)).decode()
        new_user = User.objects.create(
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user'] = new_user.fname
        request.session['id'] = new_user.id
        return redirect('/dashboard')
    
    
    
def dashboard(request):
    if 'user' not in request.session:
        messages.errors(request, "You must be logged in")
        return redirect('/')
    context = {
        "time": strftime("%Y-%m-%d %H:%M %p", localtime()),
        "events": Event.objects.all()
    }
    return render(request, 'dashboard.html', context)



def postEvent(request):
    errors = Event.objects.event_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        Event.objects.create(
            event = request.POST['event'],
            location = request.POST['location'],
            head_count = request.POST['head_count'],
            time = request.POST['time'],
            date = request.POST['date'],
            user_event = User.objects.get(id=request.session['id'])
        )
        return redirect('/dashboard')



def account(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    
    return render(request, "account.html", context)



def logout(request):
    request.session.flush()
    return redirect('/')

