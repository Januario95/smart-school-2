# Generated by Django 4.1.6 on 2023-05-31 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0035_alter_classenewmodel_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classenewmodel',
            options={'ordering': ('id',), 'verbose_name': 'Classe', 'verbose_name_plural': 'Classes'},
        ),
    ]
