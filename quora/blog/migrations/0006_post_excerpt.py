# Generated by Django 3.0.2 on 2021-04-23 14:02

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210423_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
