# Generated by Django 5.0.2 on 2024-04-13 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 13, 15, 45, 6, 42958)),
        ),
        migrations.AlterField(
            model_name='blog',
            name='level',
            field=models.TextField(default='Premium1'),
        ),
    ]