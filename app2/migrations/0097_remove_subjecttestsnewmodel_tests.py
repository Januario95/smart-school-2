# Generated by Django 4.1.6 on 2023-06-26 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0096_parentnamenewmodel_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjecttestsnewmodel',
            name='tests',
        ),
    ]
