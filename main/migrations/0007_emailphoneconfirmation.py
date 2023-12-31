# Generated by Django 4.2.3 on 2023-10-02 06:41

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_authtokens_exp_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailPhoneConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=25, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
            ],
        ),
    ]
