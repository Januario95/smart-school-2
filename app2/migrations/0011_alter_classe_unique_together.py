# Generated by Django 4.1.6 on 2023-03-13 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0010_alter_classe_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classe',
            unique_together={('name', 'turma')},
        ),
    ]