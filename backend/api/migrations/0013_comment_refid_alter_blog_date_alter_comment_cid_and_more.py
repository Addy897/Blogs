# Generated by Django 5.0.2 on 2024-04-11 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_comment_alter_blog_date_alter_eusers_pfphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='refId',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 11, 18, 30, 15, 966233)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.UUIDField(default='4a83d296-579c-5314-b8af-284675fcd29a'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 11, 18, 30, 15, 966233)),
        ),
    ]
