# Generated by Django 5.1.3 on 2025-05-06 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0058_alter_post_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=150),
        ),
    ]
