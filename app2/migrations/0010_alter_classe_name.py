# Generated by Django 4.1.6 on 2023-03-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0009_parent_email_student_email_teacher_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classe',
            name='name',
            field=models.CharField(max_length=11),
        ),
    ]
