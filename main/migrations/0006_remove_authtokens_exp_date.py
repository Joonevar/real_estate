# Generated by Django 4.2.3 on 2023-10-02 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_authtokens_token_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authtokens',
            name='exp_date',
        ),
    ]