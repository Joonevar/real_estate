# Generated by Django 4.2.3 on 2023-10-02 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_emailphoneconfirmation_exp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtokens',
            name='device',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
