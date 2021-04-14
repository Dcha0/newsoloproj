
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('loggingIn', views.loggingIn),
    path('to-validate', views.registration),
    path('dashboard', views.dashboard),
    path('postEvent', views.postEvent),
    path('user-info', views.account),
    path('logging-out', views.logout),
    ]
