# Generated by Django 4.1.6 on 2023-06-25 22:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0094_teacherschoolattended_degree'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teachernamenewmodel',
            options={'ordering': ('-created_at',), 'verbose_name': 'Teacher New', 'verbose_name_plural': 'Teachers New'},
        ),
        migrations.AddField(
            model_name='teachernamenewmodel',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='teachernamenewmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
