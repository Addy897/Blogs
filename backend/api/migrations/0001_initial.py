# Generated by Django 5.0.2 on 2024-04-10 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=24)),
                ('password', models.CharField(max_length=100)),
                ('pfPhoto', models.CharField(max_length=256)),
            ],
        ),
    ]
