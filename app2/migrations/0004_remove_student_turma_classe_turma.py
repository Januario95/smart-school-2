# Generated by Django 4.1.6 on 2023-03-12 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0003_alter_classe_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='turma',
        ),
        migrations.AddField(
            model_name='classe',
            name='turma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.turma'),
        ),
    ]
