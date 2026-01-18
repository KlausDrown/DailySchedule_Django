from django.db import models
from django.conf import settings
from django.utils import timezone


class DailySchedule(models.Model):
    """Модель для хранения расписания на день"""
    
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    
    
    date = models.DateField(db_index=True)
    

    priority = models.PositiveSmallIntegerField(
        default=0,
        help_text="Приоритет дня (чем выше значение, тем выше приоритет)"
    )
    
    
    total_tasks = models.PositiveIntegerField(default=0)
    total_minutes = models.PositiveIntegerField(default=0)

    
    schedule_data = models.JSONField(default=dict)
    
    
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_schedules'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_schedules'
    )
    
    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения.
        Автоматически устанавливает created_by при создании.
        """
        
        if not self.pk and self.created_by is None:
            self.created_by = self.user
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    class Meta:
        verbose_name = "Расписание на день"
        verbose_name_plural = "Расписания на дни"
        ordering = ['-date', '-priority']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', '-date']),  
            models.Index(fields=['date']),  
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'],
                name='unique_schedule_per_user_per_day'
            ),
        ]