# Generated by Django 2.0.3 on 2018-04-14 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buysell', '0015_remove_buypost_time_diff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='received',
            old_name='time',
            new_name='date_posted',
        ),
        migrations.RenameField(
            model_name='sent',
            old_name='time',
            new_name='date_posted',
        ),
    ]
