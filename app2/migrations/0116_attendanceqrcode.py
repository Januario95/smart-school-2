# Generated by Django 4.1.6 on 2023-06-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0115_studentattendance_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceQRcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/')),
            ],
        ),
    ]
