# Generated by Django 5.1.3 on 2025-04-12 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0034_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='/default.jpg', upload_to='thumnail_post'),
        ),
    ]
