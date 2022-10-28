from django.db import models
from django.utils.timezone import now


class Rows(models.Model):
    uuid = models.CharField(max_length=255)
    oneCId = models.IntegerField(unique=True)
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=20)
    catNumber = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    isDone = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    dateCreated = models.DateField(auto_now_add=True, blank=True)
    dateChanged = models.DateField(auto_now=True, blank=True)
    videoUrl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Карточка в Работе"

    def __str__(self):
        return self.name
