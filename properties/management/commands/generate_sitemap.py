# properties/management/commands/generate_sitemap.py
import json
from django.core.management.base import BaseCommand
from properties.models import Location
from collections import defaultdict

class Command(BaseCommand):
    help = 'Generate a sitemap.json file for country locations'

    def handle(self, *args, **kwargs):
        # Create a defaultdict to group locations by country
        countries = defaultdict(list)

        # Query all locations and group them by country
        locations = Location.objects.all().order_by('title')  # Sorting by location name

        for location in locations:
            country_slug = location.country_code.lower()  # You can modify this as needed
            countries[country_slug].append({
                location.title: f'{country_slug}/{location.slug}'
            })

        # Now create the final JSON structure
        sitemap = []
        for country_slug, locations in countries.items():
            # Retrieve country name from a predefined list or map (modify as necessary)
            country_name = self.get_country_name(country_slug)

            sitemap.append({
                country_name: country_slug,
                "locations": locations
            })

        # Write the sitemap to a JSON file
        with open('sitemap.json', 'w') as file:
            json.dump(sitemap, file, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))

    def get_country_name(self, country_slug):
        # Modify this method to map country_slug to the country name
        country_mapping = {
            'usa': 'USA',
            'bd': 'Bangladesh',
            # Add more countries here as needed
        }
        return country_mapping.get(country_slug, country_slug)  # Default to slug if not found
