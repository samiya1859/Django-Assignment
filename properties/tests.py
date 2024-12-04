from django.test import TestCase
from django.contrib.gis.geos import Point
from django.urls import reverse
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from .models import Location,Amenity,Accommodation,LocalizedAccommodation
# Create your tests here.

# for location model
class LocationModelTest(TestCase):

    def test_create_location(self):
        # Create a location
        location = Location.objects.create(
            title='Test Location',
            slug='test-location',
            center=Point(1.0, 1.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='Los Angeles'
        )
        
        # Check if the location is saved correctly
        self.assertEqual(location.title, 'Test Location')
        self.assertEqual(location.slug, 'test-location')
        self.assertEqual(location.location_type, 'city')
        self.assertEqual(location.country_code, 'US')
        self.assertEqual(location.state_abbr, 'CA')
        self.assertEqual(location.city, 'Los Angeles')
        self.assertEqual(location.center.x, 1.0)  
        self.assertEqual(location.center.y, 1.0)  
        self.assertEqual(str(location), 'Test Location - city')

# for amenity model 
class AmenityModelTest(TestCase):

    def test_create_amenity(self):
        
        amenity = Amenity.objects.create(amenity='Swimming Pool')
        self.assertEqual(amenity.amenity, 'Swimming Pool')
        self.assertEqual(str(amenity), 'Swimming Pool')


# for Accomodation model 
class AccommodationModelTest(TestCase):

    def test_create_accommodation(self):
        # Create a location for the accommodation
        location = Location.objects.create(
            title='Test Location',
            slug='test-location',
            center=Point(1.0, 1.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='Los Angeles'
        )
        
        # Create an accommodation
        accommodation = Accommodation.objects.create(
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(1.0, 1.0),  # Same coordinates as the location
            location=location,
            user=None,  # Assuming user is optional for this test
            published=True
        )
        
        
        self.assertEqual(accommodation.title, 'Test Accommodation')
        self.assertEqual(accommodation.country_code, 'US')
        self.assertEqual(accommodation.bedroom_count, 2)
        self.assertEqual(accommodation.review_score, 4.5)
        self.assertEqual(accommodation.usd_rate, 100.00)
        self.assertEqual(accommodation.published, True)
        self.assertEqual(accommodation.center.x, 1.0)  
        self.assertEqual(accommodation.center.y, 1.0) 
        self.assertEqual(str(accommodation), 'Test Accommodation - US')

#for localized accomodation model
class LocalizedAccommodationModelTest(TestCase):

    def test_create_localized_accommodation(self):
        # Create an accommodation
        accommodation = Accommodation.objects.create(
            title='Test Property',
            country_code='US',
            bedroom_count=3,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(1.0, 1.0),
            location=Location.objects.create(
                title='Test Location',
                slug='test-location',
                center=Point(1.0, 1.0),
                location_type='city',
                country_code='US',
                state_abbr='CA',
                city='Los Angeles'
            )
        )
        
        # Create a localized accommodation
        localized = LocalizedAccommodation.objects.create(
            property=accommodation,
            language='en',
            description='A beautiful place',
            policy={'cancellation': 'no refund'}
        )
        
        # Check if the localized accommodation is saved correctly
        self.assertEqual(localized.language, 'en')
        self.assertEqual(localized.description, 'A beautiful place')
        self.assertEqual(localized.policy, {'cancellation': 'no refund'})
        self.assertEqual(str(localized), 'Test Property - en')


#properties views testing

#Add property view
class AddPropertyViewTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a location for the property
        self.location = Location.objects.create(
            title='Test Location',
            center=Point(1.0, 1.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='Los Angeles'
        )

    def test_add_property_valid(self):
        data = {
            'title': 'Test Property',
            'country_code': 'US',
            'bedroom_count': 3,
            'review_score': 4.5,
            'usd_rate': 150.00,
            'location': self.location.id,
            'center': '1.0,1.0',
            'published': True,
        }

        response = self.client.post(reverse('add_property'), data)

        # Check if the property is created successfully
        property = Accommodation.objects.first()
        self.assertEqual(property.title, 'Test Property')
        self.assertEqual(property.center.x, 1.0)  
        self.assertEqual(property.center.y, 1.0) 

    def test_add_property_invalid(self):
        # Missing required field: 'title'
        data = {
            'country_code': 'US',
            'bedroom_count': 3,
            'review_score': 4.5,
            'usd_rate': 150.00,
            'location': self.location.id,
            'center': '1.0,1.0',
            'published': True,
        }

        response = self.client.post(reverse('add_property'), data)

        # Ensure we get the template with the form
        self.assertEqual(response.status_code, 200)


# testing property detail view
class PropertyDetailViewTest(TestCase):
    
    def setUp(self):
        # Set up test data, such as creating a user and a property
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123', email='testuser@example.com'
        )
        
        self.location = Location.objects.create(
            title="Test Location", location_type="City", country_code="US", state_abbr="CA", 
            city="TestCity", center=Point(1.0, 1.0)
        )
        
        image_path = os.path.join(settings.BASE_DIR, 'interfaces', 'media', '5.jpg')

    # Open the image file
        with open(image_path, 'rb') as img_file:
            self.test_image = File(img_file)
            # Save the image using Django's default storage
            self.test_image.name = '5.jpg'  # Set the file name for storage
            self.test_image = default_storage.save(self.test_image.name, self.test_image)
            self.test_image_url = default_storage.url(self.test_image)
    

            
        # Create an Accommodation instance without an image
        self.accommodation = Accommodation.objects.create(
            title="Test Property", country_code="US", bedroom_count=2, review_score=4.5, 
            usd_rate=100.0, center=Point(1.0, 1.0), location=self.location, user=self.user, 
            published=True,
            main_image=self.test_image,
        )
        
        # Create a LocalizedAccommodation with policy data
        self.localized_accommodation = LocalizedAccommodation.objects.create(
            property=self.accommodation, language='en', 
            description="Test description", 
            policy={"cancellation": "Free cancellation", "check_in": "2:00 PM"}
        )
    
        self.url = reverse('property_detail', kwargs={'pk': self.accommodation.pk})
    def test_property_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.accommodation.title)
        self.assertContains(response, self.accommodation.main_image.url)


# updating property view testing
class PropertyUpdateViewTest(TestCase):
    
    def setUp(self):
        # Create test user and login
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        
        # Create a valid Location object
        self.location = Location.objects.create(
            title='Test Location', 
            country_code='US', 
            state_abbr='CA', 
            city='Test City', 
            location_type='city', 
            center=Point(-118.2437, 34.0522)  # Add a valid Point for center
        )

        # Create the Accommodation object with a valid center point
        self.accommodation = Accommodation.objects.create(
            title='Test Property',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(-118.2437, 34.0522),  # Add a valid Point for center
            location=self.location,
            user=self.user,
            published=True,
        )
        self.url = reverse('edit_property', kwargs={'pk': self.accommodation.pk})
        self.client.login(username='testuser', password='password123')

    def test_property_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addproperty.html')

    def test_property_update_view_post_valid(self):
    # Prepare the updated data
        data = {
            'title': 'Updated Property Title',
            'country_code': 'US',
            'bedroom_count': 2,
            'review_score': 4.5,
            'usd_rate': 200.00,  # Updated price
            'center': 'POINT(-118.2437 34.0522)',  # Valid Point (latitude, longitude)
            'location': self.location.id,  # Make sure to reference the correct location ID
            'published': True,
        }
    
        # Make the POST request with the updated data
        response = self.client.post(self.url, data)
    
        # Refresh the object to get the latest data from the database
        self.accommodation.refresh_from_db()
    
        # Check for the correct response and that the object was updated
        self.assertEqual(response.status_code, 302)  # Expecting redirect (success)
        self.assertEqual(self.accommodation.title, 'Updated Property Title')
        self.assertEqual(self.accommodation.usd_rate, 200.00)
        self.assertEqual(self.accommodation.published, True)
    
    def test_property_update_view_success_url(self):
        data = {
            'title': 'Updated Property Title',
            'country_code': 'US',
            'bedroom_count': 2,
            'review_score': 4.5,
            'usd_rate': 200.00,
            'center': 'POINT(-118.2437 34.0522)',  # Valid Point
            'location': self.location.id,
            'published': True,
        }
        response = self.client.post(self.url, data)
        
        # Manually check the redirect URL instead of using reverse
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/properties/') 