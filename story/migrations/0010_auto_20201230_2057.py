# Generated by Django 3.1.3 on 2020-12-30 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0009_auto_20201230_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
    ]
