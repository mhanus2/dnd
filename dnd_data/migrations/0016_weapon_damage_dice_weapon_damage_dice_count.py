# Generated by Django 4.2.4 on 2023-11-15 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dnd_data', '0015_remove_alignment_created_remove_background_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapon',
            name='damage_dice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dnd_data.dice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weapon',
            name='damage_dice_count',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
