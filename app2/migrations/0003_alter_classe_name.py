# Generated by Django 4.1.6 on 2023-03-12 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0002_alter_classe_options_alter_subjectname_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classe',
            name='name',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]