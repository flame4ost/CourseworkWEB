# Generated by Django 3.1.7 on 2021-04-06 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0004_parkingspot_destination'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinginfo',
            name='notifid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
