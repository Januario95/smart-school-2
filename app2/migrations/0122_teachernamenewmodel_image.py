# Generated by Django 4.1.6 on 2023-07-02 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0121_alter_testnewmodel_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachernamenewmodel',
            name='image',
            field=models.ImageField(default='/media/profile_image2.png', upload_to='profiles/%y%m%d'),
        ),
    ]