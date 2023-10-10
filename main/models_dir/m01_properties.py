from django.db import models
from main.models_dir import m02_users

class Property(models.Model):

    name                    = models.CharField(max_length = 120, blank = True, null = True)
    price                   = models.IntegerField(blank = True, null = True)
    cur                     = models.CharField(max_length = 4, blank = True, null = True)

    upload_date             = models.DateField(blank = True, null = True)

    details                 = models.TextField(max_length = 1024, blank = True, null = True)

    number_of_rooms         = models.IntegerField(blank = True, null = True)
    number_of_bathroom      = models.IntegerField(blank = True, null = True)
    category                = models.CharField(max_length = 120, blank = True, null = True)
    property_type           = models.CharField(max_length = 120, blank = True, null = True)
    floor_space             = models.CharField(max_length = 32, blank = True, null = True)
    land_area               = models.CharField(max_length = 32, blank = True, null = True)
    condition               = models.CharField(max_length = 120, blank = True, null = True)
    year_of_construction    = models.CharField(max_length = 25, blank = True, null = True)
    building_levels         = models.IntegerField(blank = True, null = True)
    elevator                = models.BooleanField(blank = True, default = False)
    heating                 = models.CharField(max_length = 120, blank = True, null = True)
    views                   = models.CharField(max_length = 120, blank = True, null = True)
    orientation             = models.CharField(max_length = 120, blank = True, null = True)
    interior_height         = models.CharField(max_length = 120, blank = True, null = True)
    air_condition           = models.BooleanField(blank = True, default = False)
    attic                   = models.CharField(max_length = 120, blank = True, null = True)
    parking                 = models.CharField(max_length = 120, blank = True, null = True)
    balcony                 = models.BooleanField(blank = True, default = False)
    bathroom_toilet         = models.CharField(max_length = 120, blank = True, null = True)
    images_videos           = models.ManyToManyField("PropertyImagesVideos", blank = True)
    extra_features          = models.TextField(blank = True, null = True)

    country                 = models.CharField(max_length = 256, blank = True, null = True)
    city                    = models.CharField(max_length = 256, blank = True, null = True)
    address                 = models.CharField(max_length = 1024, blank = True, null = True)

    document                = models.FileField(blank = True, null = True)
    approved                = models.BooleanField(blank = True, default = False)

    lister                  = models.ForeignKey(m02_users.CustomUser, on_delete = models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        return self.name





class PropertyImagesVideos(models.Model):
    file                    = models.FileField(upload_to = "images_videos", blank = True, null = True)
    file_type               = models.CharField(max_length = 32, blank = True, null = True)

    def __str__(self) -> str:
        return f"{self.file_type}_{self.id}"