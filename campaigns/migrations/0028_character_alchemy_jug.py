# Generated by Django 4.2.4 on 2023-11-15 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0027_characterweapon_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='alchemy_jug',
            field=models.SmallIntegerField(default=0),
        ),
    ]
