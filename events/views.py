from django.shortcuts import render, redirect
import bcrypt
import datetime
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



def updateProfile(request, id):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/user-info')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(8)).decode()
        user = User.objects.get(id=id)
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.password = pw_hash
        user.save()
        return redirect('/user-info')



def dashboard(request):
    if 'user' not in request.session:
        messages.errors(request, "You must be logged in")
        return redirect('/')
    today = datetime.date.today()
    this_user = User.objects.get(id=request.session['id'])
    context = {
        "today_event": this_user.join_events.filter(date=today),
        "time": strftime("%m-%d-%Y", localtime()),
        "events": Event.objects.all(),
        "user": this_user
    }
    return render(request, 'dashboard.html', context)



def postEvent(request):
    errors = Event.objects.event_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        user = User.objects.get(id=request.session['id'])
        event = Event.objects.create(
            event = request.POST['event'],
            location = request.POST['location'],
            head_count = request.POST['head_count'],
            time = request.POST['time'],
            date = request.POST['date'],
            user_event = user
        )
        user.join_events.add(event)
        return redirect('/dashboard')



def eventPage(request):
    if 'user' not in request.session:
        messages.error(request, "Please sign in or sign up to view this page")
        return redirect('/')
    context = {
        'events': Event.objects.all().order_by('date'),
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, "eventPage.html", context)



def eventInfo(request, id):
    context = {
        "event": Event.objects.get(id=id)
    }
    
    return render(request, "eventInfo.html", context)


def account(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, "account.html", context)



def profile(request, id):
    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, "profile.html", context)


def joinEvent(request, id):
    user = User.objects.get(id=request.session["id"])
    event = Event.objects.get(id=id)
    user.join_events.add(event)
    messages.success(request, "Event has been added")
    return redirect('/allEvents')



def cancelEvent(request, id):
    user = User.objects.get(id=request.session['id'])
    event = Event.objects.get(id=id)
    user.join_events.remove(event)
    messages.success(request, "Event has been canceled")
    return redirect('/dashboard')


def logout(request):
    request.session.flush()
    messages.success(request, "You have successfully logged out")
    return redirect('/')


def deleteUser(request, id):
    user = User.objects.get(id=request.session['id'])
    user.delete()
    messages.success(request, "You have successfully deleted your account")
    return redirect('/')


def deleteEvent(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request, "Event has been delete")
    return redirect('/user-info')