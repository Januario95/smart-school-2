# Generated by Django 4.1.6 on 2023-03-15 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0017_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='subjects',
            field=models.ManyToManyField(to='app2.subjectname'),
        ),
    ]
