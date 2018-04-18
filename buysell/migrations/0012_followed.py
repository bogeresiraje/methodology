# Generated by Django 2.0.3 on 2018-04-09 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buysell', '0011_auto_20180403_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pub_time', models.DateTimeField(verbose_name='date added')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buysell.Account')),
            ],
        ),
    ]