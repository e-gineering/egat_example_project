# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Processing'), (1, b'Processed')])),
                ('card_type', models.CharField(default=b'visa', max_length=40, choices=[(b'visa', b'Visa'), (b'mast', b'Mastercard'), (b'disc', b'Discover')])),
                ('card_number', models.CharField(max_length=16)),
                ('expiration_date', models.CharField(max_length=7)),
                ('ccv', models.CharField(max_length=4)),
                ('order', models.ForeignKey(to='order_manager.Order')),
            ],
        ),
    ]
