# Generated by Django 4.2.4 on 2023-10-14 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0012_character_magical_property_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='created',
        ),
    ]
