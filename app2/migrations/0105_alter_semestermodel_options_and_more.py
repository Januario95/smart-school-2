# Generated by Django 4.1.6 on 2023-06-28 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0104_alter_parentnamenewmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semestermodel',
            options={'verbose_name': 'Semester', 'verbose_name_plural': 'Semester'},
        ),
        migrations.AlterModelOptions(
            name='semesternewmodel',
            options={'verbose_name': 'Semester Name', 'verbose_name_plural': 'Semester Names'},
        ),
    ]