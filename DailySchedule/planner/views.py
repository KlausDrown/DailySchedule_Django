from django.shortcuts import render

# Create your views here.
def indexCalendar(request):
    return render(request, "web/calendar.html")
def dailySchedule(request):
    return render(request, "web/dailySchedule.html")