# Generated by Django 4.1.6 on 2023-06-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0103_alter_studentnamenewmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parentnamenewmodel',
            options={'ordering': ('-created_at',), 'verbose_name': 'Parent', 'verbose_name_plural': 'Parents'},
        ),
        migrations.AddField(
            model_name='parentnamenewmodel',
            name='numero_de_bi',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
