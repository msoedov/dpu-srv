# Generated by Django 3.1 on 2021-07-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210723_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='new_count',
            field=models.IntegerField(default=0),
        ),
    ]
