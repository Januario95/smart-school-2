# Generated by Django 4.1.6 on 2023-06-29 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0112_attendanceurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjecttestsnewmodel',
            name='link_is_open',
            field=models.BooleanField(default=False),
        ),
    ]
