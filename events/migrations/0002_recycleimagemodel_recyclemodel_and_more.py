# Generated by Django 4.1.3 on 2022-12-24 10:09

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecycleImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('image', models.ImageField(upload_to='recycles')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecycleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('geocode', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('recycle_types', multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Scrap metal'), ('2', 'Waste paper'), ('3', 'Glass'), ('4', 'Mechanism'), ('5', 'Furniture'), ('6', 'Plastic')], max_length=20)),
                ('working_days', multiselectfield.db.fields.MultiSelectField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], max_length=20)),
                ('opening', models.TimeField()),
                ('closing', models.TimeField()),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='recyclemodel',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created_at', 'updated_at'], name='events_recy_created_503578_brin'),
        ),
        migrations.AddField(
            model_name='recycleimagemodel',
            name='recycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='events.recyclemodel'),
        ),
        migrations.AddIndex(
            model_name='recycleimagemodel',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created_at', 'updated_at'], name='events_recy_created_8cce81_brin'),
        ),
    ]