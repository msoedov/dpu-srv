# Generated by Django 3.1 on 2021-07-23 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_events_new_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='space',
            old_name='comany',
            new_name='company',
        ),
    ]
