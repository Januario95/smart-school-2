# Generated by Django 4.1.6 on 2023-03-12 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('8ª classe', '8ª Classe'), ('9ª classe', '9ª Classe'), ('10ª classe', '10ª Classe'), ('11ª classe', '11ª Classe'), ('12ª classe', '12ª Classe')], default='12ª classe', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mark', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.subjectname')),
                ('tests', models.ManyToManyField(blank=True, to='app2.test')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('numero_de_bi', models.CharField(blank=True, max_length=13)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6)),
                ('birth_date', models.DateField()),
                ('province', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=50)),
                ('bairro', models.CharField(blank=True, max_length=50)),
                ('quarteirao', models.CharField(blank=True, max_length=100)),
                ('father_name', models.CharField(blank=True, max_length=150)),
                ('mother_name', models.CharField(blank=True, max_length=150)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.classe')),
                ('subjects', models.ManyToManyField(blank=True, to='app2.subjectmark')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app2.turma')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
    ]
