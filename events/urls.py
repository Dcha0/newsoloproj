
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('loggingIn', views.loggingIn),
    path('to-validate', views.registration),
    path('dashboard', views.dashboard),
    path('postEvent', views.postEvent),
    path('allEvents', views.eventPage),
    path('event-info/<int:id>', views.eventInfo),
    path('user-info', views.account),
    path('user-profile/<int:id>', views.profile),
    path('update-info/<int:id>', views.updateProfile),
    path('join-event/<int:id>', views.joinEvent),
    path('cancel-event/<int:id>', views.cancelEvent),
    path('logging-out', views.logout),
    path('delete-me/<int:id>', views.deleteUser),
    path('delete-event/<int:id>', views.deleteEvent)
]
