# Generated by Django 3.2.6 on 2021-08-27 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_otp_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
