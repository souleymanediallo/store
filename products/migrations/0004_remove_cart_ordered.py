# Generated by Django 5.0 on 2023-12-10 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='ordered',
        ),
    ]
