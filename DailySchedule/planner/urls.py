from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('api/schedule/', views.ScheduleView.as_view(), name='schedule_create'),
    path('day', login_required(TemplateView.as_view(template_name="web/dailySchedule.html")), name='dailySchedule'),
    path('', TemplateView.as_view(template_name="web/calendar.html"), name='indexCalendar'),
]