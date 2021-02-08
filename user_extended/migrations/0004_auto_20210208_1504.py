# Generated by Django 3.1 on 2021-02-08 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemon', '0003_delete_favouriteitem'),
        ('user_extended', '0003_auto_20210208_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='cart_items',
        ),
        migrations.AlterField(
            model_name='profile',
            name='favourite_items',
            field=models.ManyToManyField(to='lemon.Item'),
        ),
    ]
