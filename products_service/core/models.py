from django.db import models
from django.core.validators import MinValueValidator as Min

class Product(models.Model):
    name        = models.CharField(max_length=40)
    description = models.TextField()
    price       = models.IntegerField(validators=[Min(-1)])

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
