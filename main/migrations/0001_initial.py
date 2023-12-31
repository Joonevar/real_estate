# Generated by Django 4.2.3 on 2023-10-01 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('bio', models.TextField(blank=True, max_length=512, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('phone_confirmed', models.BooleanField(blank=True, default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('email_confirmed', models.BooleanField(blank=True, default=False)),
                ('country', models.CharField(blank=True, max_length=256, null=True)),
                ('city', models.CharField(blank=True, max_length=256, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyImagesVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='images_videos')),
                ('file_type', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('cur', models.CharField(blank=True, max_length=4, null=True)),
                ('details', models.TextField(blank=True, max_length=1024, null=True)),
                ('number_of_rooms', models.IntegerField(blank=True, null=True)),
                ('number_of_bathroom', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=120, null=True)),
                ('property_type', models.CharField(blank=True, max_length=120, null=True)),
                ('floor_space', models.CharField(blank=True, max_length=32, null=True)),
                ('land_area', models.CharField(blank=True, max_length=32, null=True)),
                ('condition', models.CharField(blank=True, max_length=120, null=True)),
                ('year_of_construction', models.CharField(blank=True, max_length=25, null=True)),
                ('building_levels', models.CharField(blank=True, max_length=120, null=True)),
                ('elevator', models.BooleanField(blank=True, default=False)),
                ('heating', models.CharField(blank=True, max_length=120, null=True)),
                ('views', models.CharField(blank=True, max_length=120, null=True)),
                ('orientation', models.CharField(blank=True, max_length=120, null=True)),
                ('interior_height', models.CharField(blank=True, max_length=120, null=True)),
                ('air_condition', models.BooleanField(blank=True, default=False)),
                ('attic', models.CharField(blank=True, max_length=120, null=True)),
                ('parking', models.CharField(blank=True, max_length=120, null=True)),
                ('balcony', models.BooleanField(blank=True, default=False)),
                ('bathroom_toilet', models.CharField(blank=True, max_length=120, null=True)),
                ('extra_features', models.JSONField(blank=True)),
                ('country', models.CharField(blank=True, max_length=256, null=True)),
                ('city', models.CharField(blank=True, max_length=256, null=True)),
                ('address', models.CharField(blank=True, max_length=1024, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='')),
                ('approved', models.BooleanField(blank=True, default=False)),
                ('images_videos', models.ManyToManyField(blank=True, to='main.propertyimagesvideos')),
                ('lister', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
