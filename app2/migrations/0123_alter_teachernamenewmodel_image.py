# Generated by Django 4.1.6 on 2023-07-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0122_teachernamenewmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachernamenewmodel',
            name='image',
            field=models.ImageField(default='/media/profile_image2.jpg', upload_to='profiles/%y%m%d'),
        ),
    ]
