from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexCalendar),
    path('day', views.dailySchedule),
]