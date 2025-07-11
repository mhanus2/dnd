# Generated by Django 4.2.4 on 2023-11-01 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dnd_data', '0012_alter_item_allowed_characters'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpellComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SpellSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SpellType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('casting_time', models.CharField(max_length=10)),
                ('range', models.CharField(max_length=10)),
                ('duration', models.CharField(max_length=25)),
                ('components', models.ManyToManyField(related_name='spells', to='dnd_data.spellcomponent')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='dnd_data.spellschool')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='dnd_data.spelltype')),
            ],
        ),
    ]
