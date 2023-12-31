# Generated by Django 5.0 on 2023-12-17 20:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_shippingaddress_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
