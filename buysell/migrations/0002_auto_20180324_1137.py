# Generated by Django 2.0.3 on 2018-03-24 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buysell', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
