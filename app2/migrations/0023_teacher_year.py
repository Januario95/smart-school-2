# Generated by Django 4.1.6 on 2023-03-21 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0022_teacher_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]