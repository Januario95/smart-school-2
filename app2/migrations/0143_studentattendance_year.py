# Generated by Django 4.1.6 on 2023-07-05 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0142_studentattendance_classe'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentattendance',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.year'),
        ),
    ]
