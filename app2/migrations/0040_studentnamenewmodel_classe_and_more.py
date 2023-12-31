# Generated by Django 4.1.6 on 2023-05-31 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0039_alter_studentnamenewmodel_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentnamenewmodel',
            name='classe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.classenewmodel'),
        ),
        migrations.AddField(
            model_name='studentnamenewmodel',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.semesternewmodel'),
        ),
        migrations.AddField(
            model_name='studentnamenewmodel',
            name='turma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.turmanewmodel'),
        ),
    ]
