# Generated by Django 3.1.2 on 2020-11-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20201102_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='عنوان'),
        ),
    ]
