# Generated by Django 4.2.3 on 2023-10-02 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_property_upload_date_authtokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtokens',
            name='token_type',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]