# Generated by Django 3.1.6 on 2021-07-17 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0002_auto_20210716_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]