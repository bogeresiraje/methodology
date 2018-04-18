# Generated by Django 2.0.3 on 2018-04-17 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buysell', '0020_auto_20180416_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='buycomment',
            name='publisher',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='sellcomment',
            name='publisher',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='buycomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buysell.Buypost'),
        ),
        migrations.AlterField(
            model_name='sellcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buysell.Sellpost'),
        ),
    ]
