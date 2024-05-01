# Generated by Django 5.0.2 on 2024-05-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_blog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.TextField(choices=[('Draft', 'Draft 1'), ('InReview', 'InReview 1'), ('Published', 'Published 1')], default='Draft', max_length=20),
        ),
    ]
