from django.db import models

class Points(models.Model):
    user_id = models.CharField(max_length=200)
    point = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
