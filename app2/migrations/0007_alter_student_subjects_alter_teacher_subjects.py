# Generated by Django 4.1.6 on 2023-03-12 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0006_alter_teacher_options_alter_student_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='app2.subjectmark'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='app2.subjectname'),
        ),
    ]