# Generated by Django 4.1.6 on 2023-06-28 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0102_alter_studentnamenewmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentnamenewmodel',
            options={'ordering': ('-created_at',), 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
    ]
