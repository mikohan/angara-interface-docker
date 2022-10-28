from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from transliterate import translit
from django.utils.text import slugify


class CompanyPages(models.Model):

    title = models.CharField(max_length=255)

    textHTML = RichTextUploadingField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Страницa Компании"
        verbose_name_plural = "Страницы Компании"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, "ru", reversed=True))
        super().save(*args, **kwargs)
