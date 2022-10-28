from django.db import models

class Documentation(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = 'Документация'
        verbose_name_plural = 'Документация'

    def __str__(self):
        return self.title
