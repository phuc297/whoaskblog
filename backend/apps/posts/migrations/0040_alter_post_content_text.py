# Generated by Django 5.1.3 on 2025-04-12 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0039_alter_post_content_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_text',
            field=models.TextField(blank=True),
        ),
    ]
