# Generated by Django 4.1.6 on 2023-03-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0015_parent_is_male'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectname',
            name='year',
            field=models.CharField(default='2023', max_length=4),
        ),
    ]
