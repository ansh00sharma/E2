# Generated by Django 5.1.1 on 2024-09-22 11:42

import servers.models
import servers.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_category_icon_alter_server_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=servers.models.channel_banner_upload_path, validators=[servers.validators.validate_icon_for_channel]),
        ),
        migrations.AddField(
            model_name='channel',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='', validators=[servers.validators.validate_icon_for_channel], verbose_name=servers.models.channel_icon_upload_path),
        ),
    ]
