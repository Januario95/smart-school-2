# Generated by Django 4.1.6 on 2023-07-02 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0127_alter_teachernamenewmodel_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachernamenewmodel',
            name='profile_pic',
            field=models.ImageField(default='/profile_image2.jpg', upload_to='profiles/%Y/%m/%d'),
        ),
    ]
