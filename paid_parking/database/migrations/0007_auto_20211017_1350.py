# Generated by Django 3.2.6 on 2021-10-17 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20211017_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='total_amount',
            name='month',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='total_amount',
            name='year',
            field=models.CharField(max_length=4),
        ),
    ]
