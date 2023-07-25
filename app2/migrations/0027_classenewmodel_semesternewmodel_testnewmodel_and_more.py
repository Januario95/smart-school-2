# Generated by Django 4.1.6 on 2023-05-31 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0026_remove_subjectnamenewmodel_classe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClasseNewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SemesterNewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Primeiro', 'Primeiro'), ('Segundo', 'Segundo'), ('Terceiro', 'Terceiro')], max_length=20)),
                ('year', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='TestNewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('mark', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='TurmaNewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectNameNewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('numero_de_bi', models.CharField(blank=True, max_length=13)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6)),
                ('birth_date', models.DateField()),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('province', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=50)),
                ('bairro', models.CharField(blank=True, max_length=50)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.classenewmodel')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.semesternewmodel')),
                ('tests', models.ManyToManyField(to='app2.testnewmodel')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.turmanewmodel')),
            ],
        ),
    ]
