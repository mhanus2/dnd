# Generated by Django 4.2.4 on 2023-11-07 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dnd_data', '0014_remove_spell_type_spell_level_delete_spelltype'),
        ('campaigns', '0024_session_campaign'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterWeapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.character')),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnd_data.weapon')),
            ],
        ),
    ]
