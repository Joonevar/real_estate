# Generated by Django 4.2.3 on 2023-10-03 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_usernotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='n_type',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
