# Generated by Django 4.1.6 on 2023-06-24 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0089_rename_lecionou_teacherclassattendance_attented'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacherclassattendance',
            old_name='attented',
            new_name='attended',
        ),
    ]
