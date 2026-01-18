from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from .models import DailySchedule
from .utils.processors import ScheduleProcessor
from .forms import ScheduleForm
from django.shortcuts import render



class ScheduleView(LoginRequiredMixin, View):
    """
    Представление для обработки запросов на создание/обновление расписания
    """
    def get(self, request):
        try:
            target_date = request.GET.get('date')
            schedule = DailySchedule.objects.filter(
                user=request.user,
                date=target_date
            ).first()
            print(str(schedule.schedule_data))
            
            return JsonResponse({
                "results": [
                    {
                    "id": schedule.id,
                    "schedule_data":schedule.schedule_data
                    }
                ]
            }, status=200)
        except:
            pass

    def post(self, request):
        try:
            
            data = json.loads(request.body)
            
            schedule, created = ScheduleProcessor.process_and_save(
                data, 
                request.user,
                created_by=request.user,
                updated_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'created': created,
                'schedule': {
                    'id': schedule.id,
                    'date': schedule.date.isoformat(),
                    'user': schedule.user.username,
                    'total_tasks': schedule.total_tasks,
                    'total_minutes': schedule.total_minutes,
                    'priority': schedule.priority,
                    'created_at': schedule.created_at.isoformat() if schedule.created_at else None,
                },
                'message': 'Расписание успешно сохранено' if created else 'Расписание успешно обновлено'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Неверный формат JSON'
            }, status=400)
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        except Exception as e:
            print(f"Ошибка при сохранении расписания: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Внутренняя ошибка сервера'
            }, status=500)