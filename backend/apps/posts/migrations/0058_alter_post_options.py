# Generated by Django 5.1.3 on 2025-05-06 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0057_alter_post_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
