# Generated by Django 2.2.13 on 2020-09-28 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_closebid_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='closebid',
            name='image',
        ),
    ]