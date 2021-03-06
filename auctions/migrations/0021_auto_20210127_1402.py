# Generated by Django 3.1.4 on 2021-01-27 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20210127_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='description',
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(default=None, max_length=40),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='price',
            field=models.FloatField(),
        ),
    ]
