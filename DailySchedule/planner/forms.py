from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
import json


class ScheduleForm(forms.Form):
    """Форма для валидации данных расписания"""
    
    date = forms.DateField(required=True)
    schedule_data = forms.JSONField(required=True)
    priority = forms.IntegerField(required=False, min_value=0, initial=0)
    total_tasks = forms.IntegerField(required=False, min_value=0)
    total_minutes = forms.IntegerField(required=False, min_value=0)
    
    def clean(self):
        """Дополнительная валидация и вычисление полей"""
        cleaned_data = super().clean()
        
        
        schedule_data = cleaned_data.get('schedule_data')
        if not isinstance(schedule_data, list):
            raise ValidationError("schedule_data должен быть списком")
        
        
        if cleaned_data.get('total_tasks') is None:
            cleaned_data['total_tasks'] = len(schedule_data)
        
        if cleaned_data.get('total_minutes') is None:
            total_minutes = 0
            for task in schedule_data:
                if isinstance(task, dict):
                    total_minutes += task.get('duration_minutes', 0)
            cleaned_data['total_minutes'] = total_minutes
        
        
        for i, task in enumerate(schedule_data):
            if not isinstance(task, dict):
                raise ValidationError(f"Задача #{i+1} должна быть словарем")
            
            
            if 'name' not in task:
                raise ValidationError(f"Задача #{i+1} не содержит поле 'name'")
            
            
            if 'start_time' in task:
                try:
                    datetime.strptime(task['start_time'], '%H:%M:%S')
                except ValueError:
                    raise ValidationError(
                        f"Неверный формат времени в задаче #{i+1}: {task['start_time']}. "
                        f"Используйте формат HH:MM:SS"
                    )
        
        return cleaned_data