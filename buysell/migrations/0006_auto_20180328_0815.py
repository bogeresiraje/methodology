# Generated by Django 2.0.3 on 2018-03-28 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buysell', '0005_buypost_sellpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='buypost',
            name='time_diff',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='buypost',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
