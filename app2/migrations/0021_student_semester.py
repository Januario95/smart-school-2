# Generated by Django 4.1.6 on 2023-03-15 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0020_alter_semester_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.semester'),
        ),
    ]
