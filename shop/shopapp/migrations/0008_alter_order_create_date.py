# Generated by Django 5.1.3 on 2024-11-25 08:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_order_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
