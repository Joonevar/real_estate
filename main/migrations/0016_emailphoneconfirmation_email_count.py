# Generated by Django 4.2.3 on 2023-10-04 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_emailphoneconfirmation_sms_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailphoneconfirmation',
            name='email_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
