# Generated by Django 5.1.1 on 2024-09-14 11:46

import servers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to=servers.models.category_icon_upload_path),
        ),
        migrations.AlterField(
            model_name='server',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
