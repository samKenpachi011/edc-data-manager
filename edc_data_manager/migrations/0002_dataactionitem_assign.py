# Generated by Django 3.0.5 on 2020-04-23 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_data_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataactionitem',
            name='assign',
            field=models.CharField(default='Normal', max_length=50),
        ),
    ]
