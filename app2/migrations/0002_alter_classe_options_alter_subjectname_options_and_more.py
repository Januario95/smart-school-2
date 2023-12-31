# Generated by Django 4.1.6 on 2023-03-12 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classe',
            options={'ordering': ('id',), 'verbose_name': 'Classe', 'verbose_name_plural': 'Classes'},
        ),
        migrations.AlterModelOptions(
            name='subjectname',
            options={'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
        migrations.AlterField(
            model_name='classe',
            name='name',
            field=models.CharField(choices=[('8ª classe', '8ª Classe'), ('9ª classe', '9ª Classe'), ('10ª classe', '10ª Classe'), ('11ª classe', '11ª Classe'), ('12ª classe', '12ª Classe')], default='12ª classe', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='subjectname',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='turma',
            name='name',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
