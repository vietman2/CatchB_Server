import uuid
from django.db import models
from django.core.validators import MinValueValidator as Min

class TimeStampedModel(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(TimeStampedModel):
    name        = models.CharField(max_length=40)
    description = models.TextField()
    price       = models.IntegerField(validators=[Min(-1)])

    class Meta:
        abstract = True

class Provider(models.Model):
    uuid            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member_uuid     = models.UUIDField()

    member_name     = models.CharField(max_length=10)
    member_phone    = models.CharField(max_length=13)

    is_confirmed    = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Image(TimeStampedModel):
    image   = models.FileField()

    class Meta:
        abstract = True
