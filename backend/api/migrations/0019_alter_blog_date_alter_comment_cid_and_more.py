# Generated by Django 5.0.2 on 2024-04-11 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_blog_date_alter_comment_cid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 12, 0, 29, 29, 178852)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.UUIDField(default='9503a1b8-403d-5b97-9d84-e38fc949359f'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 12, 0, 29, 29, 178852)),
        ),
    ]
