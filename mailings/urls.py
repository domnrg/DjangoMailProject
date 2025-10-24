from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import home

app_name = MailingsConfig.name

urlpatterns = [
    path('',  home, name='home'),
]