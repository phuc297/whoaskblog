# Generated by Django 5.1.3 on 2025-04-12 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0035_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
