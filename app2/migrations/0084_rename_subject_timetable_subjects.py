# Generated by Django 4.1.6 on 2023-06-24 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0083_subjecttimetable_class_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetable',
            old_name='subject',
            new_name='subjects',
        ),
    ]
