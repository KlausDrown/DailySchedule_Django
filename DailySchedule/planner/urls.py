from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexCalendar, name='indexCalendar'),
    path('day', views.dailySchedule, name='dailySchedule'),
]