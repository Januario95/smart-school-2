# Generated by Django 4.1.6 on 2023-03-15 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0019_semester_classe'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('name', 'classe', 'year')},
        ),
    ]
