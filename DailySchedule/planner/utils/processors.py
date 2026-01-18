from django.contrib.auth import get_user_model
from django.utils import timezone
from ..forms import ScheduleForm
from ..models import DailySchedule

User = get_user_model()


class ScheduleProcessor:
    """
    Класс для обработки и сохранения данных расписания в модель DailySchedule
    """
    
    @classmethod
    def process_and_save(cls, data, user, created_by=None, updated_by=None):
        """
        Обработка данных и сохранение в модель DailySchedule
        
        Args:
            data (dict): Данные в формате словаря
            user (User): Пользователь, которому принадлежит расписание
            created_by (User, optional): Кто создал запись
            updated_by (User, optional): Кто обновил запись
            
        Returns:
            tuple: (DailySchedule объект, created булево значение)
        """
        # Валидируем данные через форму
        form = ScheduleForm(data)
        
        if not form.is_valid():
            raise ValueError(f"Ошибка валидации: {form.errors}")
        
        cleaned_data = form.cleaned_data
        
        # Проверяем, существует ли уже расписание на эту дату
        schedule, created = DailySchedule.objects.get_or_create(
            user=user,
            date=cleaned_data['date'],
            defaults={
                'priority': cleaned_data.get('priority', 0),
                'total_tasks': cleaned_data.get('total_tasks', 0),
                'total_minutes': cleaned_data.get('total_minutes', 0),
                'schedule_data': cleaned_data['schedule_data'],
                'created_by': created_by or user,
                'updated_by': updated_by or user,
            }
        )
        
        # Если запись уже существовала, обновляем ее
        if not created:
            schedule.priority = cleaned_data.get('priority', schedule.priority)
            schedule.total_tasks = cleaned_data.get('total_tasks', schedule.total_tasks)
            schedule.total_minutes = cleaned_data.get('total_minutes', schedule.total_minutes)
            schedule.schedule_data = cleaned_data['schedule_data']
            schedule.updated_by = updated_by or schedule.updated_by or user
            schedule.save()
        
        return schedule, created
    
    @classmethod
    def bulk_process_schedules(cls, schedules_data, user, created_by=None, updated_by=None):
        """
        Обработка нескольких расписаний за раз
        
        Args:
            schedules_data (list): Список словарей с данными расписаний
            user (User): Пользователь
            created_by (User, optional): Кто создал записи
            updated_by (User, optional): Кто обновил записи
            
        Returns:
            list: Список созданных/обновленных объектов DailySchedule
        """
        results = []
        for data in schedules_data:
            try:
                schedule, created = cls.process_and_save(
                    data, user, created_by, updated_by
                )
                results.append({
                    'schedule': schedule,
                    'created': created,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'schedule': None,
                    'created': False,
                    'success': False,
                    'error': str(e)
                })
        return results