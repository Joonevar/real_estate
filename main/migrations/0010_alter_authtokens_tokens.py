# Generated by Django 4.2.3 on 2023-10-03 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_authtokens_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtokens',
            name='tokens',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]