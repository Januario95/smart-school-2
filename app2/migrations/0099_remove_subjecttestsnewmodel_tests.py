# Generated by Django 4.1.6 on 2023-06-26 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0098_subjecttestsnewmodel_tests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjecttestsnewmodel',
            name='tests',
        ),
    ]
