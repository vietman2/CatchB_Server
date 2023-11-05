from django.db import models

class Schedule(models.Model):
    user_id = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schedule"
        ordering = ['date', 'time']
        verbose_name = "스케줄"
        verbose_name_plural = "스케줄"
