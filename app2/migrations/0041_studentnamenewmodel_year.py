# Generated by Django 4.1.6 on 2023-05-31 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0040_studentnamenewmodel_classe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentnamenewmodel',
            name='year',
            field=models.CharField(default=2023, max_length=4),
        ),
    ]