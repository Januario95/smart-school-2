# Generated by Django 4.1.6 on 2023-06-14 12:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app2', '0068_alter_subjectnewmodel_classe_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ParentMessageAdmin',
            new_name='ParentToAadminMessage',
        ),
    ]
