# Generated by Django 3.1.3 on 2021-01-02 18:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('story', '0012_auto_20210102_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='comment_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
