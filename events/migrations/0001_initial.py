# Generated by Django 4.1.3 on 2022-12-17 11:29

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ViolationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('geocode', models.TextField()),
                ('title', models.CharField(choices=[('1', 'Illegal Dump'), ('2', 'Deforestation'), ('3', 'Water Pollution')], max_length=20)),
                ('comment', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ViolationImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('image', models.ImageField(upload_to='violations')),
                ('violation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='events.violationmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='violationmodel',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created_at', 'updated_at'], name='events_viol_created_bdfdcf_brin'),
        ),
        migrations.AddIndex(
            model_name='violationimagemodel',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created_at', 'updated_at'], name='events_viol_created_6ecab6_brin'),
        ),
    ]
