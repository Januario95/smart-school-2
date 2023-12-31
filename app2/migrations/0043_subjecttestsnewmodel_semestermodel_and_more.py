# Generated by Django 4.1.6 on 2023-05-31 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0042_year_remove_studentnamenewmodel_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectTestsNewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.subjectnamenewmodel')),
                ('tests', models.ManyToManyField(blank=True, to='app2.testnewmodel')),
            ],
        ),
        migrations.CreateModel(
            name='SemesterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[], max_length=20)),
                ('year', models.CharField(max_length=4)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.classenewmodel')),
                ('subjects', models.ManyToManyField(to='app2.subjecttestsnewmodel')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.turmanewmodel')),
            ],
        ),
        migrations.AddField(
            model_name='studentnamenewmodel',
            name='new_semester',
            field=models.ManyToManyField(blank=True, to='app2.semestermodel'),
        ),
    ]
