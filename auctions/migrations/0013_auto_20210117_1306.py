# Generated by Django 3.1.4 on 2021-01-17 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210117_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]