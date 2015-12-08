# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20151208_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Shipping Date', blank=True, to='order.ShippingDate', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Shipping Address', blank=True, to='order.ShippingAddress', null=True),
        ),
    ]
