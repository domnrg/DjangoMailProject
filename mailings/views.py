from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView


def home(request):
    return render(request, "home.html")

#class UserListView(ListView):

