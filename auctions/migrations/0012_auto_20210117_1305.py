# Generated by Django 3.1.4 on 2021-01-17 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20210117_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
