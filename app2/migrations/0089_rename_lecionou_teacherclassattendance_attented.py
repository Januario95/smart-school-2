# Generated by Django 4.1.6 on 2023-06-24 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0088_teacherclassattendance_lecionou'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacherclassattendance',
            old_name='lecionou',
            new_name='attented',
        ),
    ]