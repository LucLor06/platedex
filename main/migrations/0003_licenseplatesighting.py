# Generated by Django 5.2.4 on 2025-07-24 04:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_licenseplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicensePlateSighting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen_on', models.DateTimeField(auto_now_add=True)),
                ('license_plate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sightings', to='main.licenseplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sightings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
