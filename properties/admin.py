from django.contrib import admin
from .models import Location, Accommodation, AccommodationImage,LocalizedAccommodation,Amenity

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at')
    list_filter = ('location_type', 'country_code', 'state_abbr', 'city')
    search_fields = ('title', 'location_type', 'country_code', 'state_abbr', 'city')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'usd_rate', 'created_at')
    list_filter = ('location', 'usd_rate')
    search_fields = ('title', 'location__title', 'usd_rate')

@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'created_at')
    list_filter = ('accommodation',)
    search_fields = ('accommodation__title',)

@admin.register(LocalizedAccommodation)
class LocalizedAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description')
    search_fields = ('property__title', 'language')
    list_filter = ('language',)
    raw_id_fields = ('property',)

admin.site.register(Amenity)