# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20150113_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.CharField(max_length=255, verbose_name='Shipping Date', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Shipping date',
                'verbose_name_plural': 'Shipping dates',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Shipping Date', blank=True, to='order.ShippingDate', null=True),
        ),
    ]
