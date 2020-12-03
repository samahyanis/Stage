from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views
from django.urls import path

urlpatterns = [
    url(r'^register/', view=views.register, name="register"),
    url(r'^login/', view=views.login, name="login"),
]
