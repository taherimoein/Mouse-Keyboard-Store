# Generated by Django 3.1.2 on 2020-11-02 05:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20201102_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=255), blank=True, null=True, size=None, verbose_name='لیست عکس های محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='top_image',
            field=models.URLField(max_length=255, null=True, verbose_name='عکس شاخص'),
        ),
    ]
