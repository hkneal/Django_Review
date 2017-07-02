from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import UserName, Trip
from .forms import login_form, register_form, add_trip_form
# Create your views here.

def getDashboardContext(id):
    user = UserName.objects.get(id=id)
    scheduled_trips = Trip.objects.filter(user=user.id).order_by('-travelDate_from')
    other_trips = Trip.objects.all().exclude(user=user.id)
    context = {
        'user' : user,
        'trips': scheduled_trips,
        'other_trips' : other_trips
    }
    return context

def index(req):
    context = {
        'login_form' : login_form(),
        'register_form' : register_form()
    }
    return render(req, 'djangoR_app/index.html', context)

def dashboard(req, id):
    user = UserName.objects.get(id=id)
    scheduled_trips = Trip.objects.filter(user=user.id).order_by('-travelDate_from')
    other_trips = Trip.objects.all().exclude(user=user.id)
    context = {
        'user' : user,
        'trips': scheduled_trips,
        'other_trips' : other_trips
    }
    return render(req, 'djangoR_app/dashboard.html', context)

def register(req):
    if req.method == 'POST':
        form = register_form(req.POST)
        if form.is_valid():
            print "Valid Registration"
            postData = {
                'name' : form.cleaned_data['name'],
                'user_name' : form.cleaned_data['user_name'],
                'password' : form.cleaned_data['password']
                }
            user = UserName.objects.register(postData)
            scheduled_trips = Trip.objects.filter(user=user['user'].id).order_by('-travelDate_from')
            other_trips = Trip.objects.all().exclude(user=user['user'].id)
            context = {
                'user' : user['user'],
                'trips': scheduled_trips,
                'other_trips' : other_trips
            }
            return render(req, 'djangoR_app/dashboard.html', context)
        else:
            context = {
                'login_form' : login_form(),
                'register_form' : form
            }
            return render(req, 'djangoR_app/index.html', context)
    else:
        return redirect('/')

def login(req):
    if req.method == 'POST':
        form = login_form(req.POST)
        if form.is_valid():
            postData = {
                'password' : form.cleaned_data['password'],
                'user_name' : form.cleaned_data['user_name']
                }
            user = UserName.objects.login(postData)
            scheduled_trips = Trip.objects.filter(user=user['user'].id).order_by('-travelDate_from')
            other_trips = Trip.objects.all().exclude(user=user['user'].id)
            context = {
                'user' : user['user'],
                'trips': scheduled_trips,
                'other_trips' : other_trips
            }
            return render(req, 'djangoR_app/dashboard.html', context)
        else:
            context = {
                'login_form' : form,
                'register_form' : register_form()
            }
            return render(req, 'djangoR_app/index.html', context)
    else:
        return redirect('/')

def add_trip(req, id):
    user = UserName.objects.get(id=id)
    if req.method == 'POST':
        form = add_trip_form(req.POST)
        if form.is_valid():
            Trip.objects.create(
                destination = form.cleaned_data['destination'],
                description = form.cleaned_data['description'],
                travelDate_from = form.cleaned_data['travelDate_from'],
                travelDate_to = form.cleaned_data['travelDate_to'],
                user = user
            )
            context = getDashboardContext(id)
            return render(req, 'djangoR_app/dashboard.html', context)
        else:
            context = {
                'add_trip_form' : form,
                'user' : user
            }
            return render(req, 'djangoR_app/add_trip.html', context)
    else:
        context = {
            'add_trip_form' : add_trip_form(),
            'user' : user
        }
        return render(req, 'djangoR_app/add_trip.html', context)

def destination(req, tid, id):
    user = UserName.objects.get(id=id)
    trip = Trip.objects.get(id=tid)
    others_lst = Trip.objects.filter(id=tid).values_list("all_users", flat=True).exclude(user=user.id)
    others = []
    if len(others_lst) > 0:
        for other in others_lst:
            others.append(UserName.objects.get(id=other).name)
    others_lst = others
    context = {
        'user' : user,
        'trip' : trip,
        'others_lst' : others_lst
    }
    return render(req, 'djangoR_app/destination.html', context)

def join_trip(req, tid, id):
    user = UserName.objects.get(id=id)
    trip = Trip.objects.get(id=tid)
    trip.all_users.add(user)
    trip.save()
    others_lst = Trip.objects.filter(id=tid).values_list("all_users", flat=True).exclude(user=user.id)
    others = []
    if len(others_lst) > 0:
        for other in others_lst:
            others.append(UserName.objects.get(id=other).name)
    others_lst = others
    context = {
        'user' : user,
        'trip' : trip,
        'others_lst' : others_lst
    }
    return render(req, 'djangoR_app/destination.html', context)
