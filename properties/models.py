from django.db import models
from autoslug import AutoSlugField
from django.contrib.gis.db import models as geomodels
from django.db.models import JSONField  
from django.utils.translation import gettext_lazy as _ 
# Create your models here.

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,null=True,blank=True)
    center = geomodels.PointField()
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=20)
    state_abbr = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.location_type}"

class Amenity(models.Model):
    amenity = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True,null=True,blank=True)

    def __str__(self):
        return self.amenity

class Accommodation(models.Model):
    id = models.AutoField(primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=20)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = geomodels.PointField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    amenities = models.ManyToManyField('Amenity', blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    main_image = models.ImageField(upload_to='', null=True, blank=True) 

    def __str__(self):
        return f"{self.title} - {self.country_code}"


class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='interfaces/media/accommodation_images/')  # Store each image file
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.accommodation.title}"
    
class LocalizedAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey('Accommodation', related_name='localized_accommodations', on_delete=models.CASCADE)
    language = models.CharField(max_length=2)  
    description = models.TextField()  
    policy = JSONField(default=dict)  

    def __str__(self):
        return f"{self.property.title} - {self.language}"

    class Meta:
        unique_together = ('property', 'language')