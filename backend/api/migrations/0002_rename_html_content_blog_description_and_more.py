# Generated by Django 5.0.2 on 2024-05-01 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='html_content',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='level',
        ),
    ]
