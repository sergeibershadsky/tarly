# Generated by Django 2.2.1 on 2019-05-21 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
