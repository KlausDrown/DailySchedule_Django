from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def indexCalendar(request):
    return render(request, "web/calendar.html")
@login_required
def dailySchedule(request):
    return render(request, "web/dailySchedule.html")