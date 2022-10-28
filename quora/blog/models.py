from django.db import models
from product.models import Category
from django.conf import settings
from ckeditor.fields import RichTextField
from product.models import Category, CarModel
from transliterate import translit
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Categories(models.Model):
    class Priority(models.IntegerChoices):
        HIGEST = 5, "Higest"
        HIGH = 4, "High"
        MEDUM = 3, "Medium"
        LOW = 2, "Low"
        LOWEST = 1, "Lowest"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    priority = models.IntegerField(
        choices=Priority.choices, default=Priority.LOWEST, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "ru", reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категоиря Блога"
        verbose_name_plural = "Категории Блога"

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=255)
    text = RichTextUploadingField(null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=settings.BLOG_IMAGES)
    parts_category = models.ManyToManyField(Category, related_name="parts_categories")
    categories = models.ManyToManyField("Categories", related_name="blog_categories")
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    author = models.CharField(max_length=100, default=settings.DEFAULT_AUTHOR)
    car = models.ManyToManyField(CarModel, related_name="post_car")
    tags = TaggableManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, "ru", reversed=True))
        super().save(*args, **kwargs)


# id: 2,
#     title: 'Logic Is The Study Of Reasoning And Argument Part 2',
#     image: '/images/posts/post-2.jpg',
#     categories: ['Latest News'],
#     date: '2019-09-05',
