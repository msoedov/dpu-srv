# Generated by Django 3.1 on 2021-07-23 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210723_0941'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='dpu',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='events',
            name='space',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='api.space'),
            preserve_default=False,
        ),
    ]