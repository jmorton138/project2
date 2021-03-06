# Generated by Django 3.1.4 on 2021-01-27 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210126_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='description',
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
