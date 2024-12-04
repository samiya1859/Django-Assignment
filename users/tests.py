from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Profile
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.utils import IntegrityError


class UserModelTest(TestCase):

    def test_user_creation(self):
        """Test that a user can be created successfully"""
        user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password123'))

    def test_user_creation_with_invalid_email(self):
        """Test that a user with invalid email raises a ValidationError"""
        with self.assertRaises(ValidationError):  
            user = get_user_model().objects.create_user(
                username='invaliduser',
                email='invalid-email',
                password='password123'
            )
            validate_email(user.email)  
    



class UserRegistrationViewTest(TestCase):

    def test_user_registration_valid(self):
        """Test that the user can register successfully"""
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123',
            'user_type': 'buyer',
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('login')) 
    

    def test_user_registration_invalid(self):
        """Test that invalid registration data is handled"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',  
            'password_confirm': 'differentpassword123', 
            'user_type': 'buyer',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
    


class UserProfileTest(TestCase):

    def setUp(self):
        """Create a user and profile for testing"""
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')

    def test_create_profile_for_user(self):
        """Test that a profile is created for the user"""
        user = self.user
        profile = Profile.objects.create(user=user, user_type='owner')  # Or any other type
    
        self.assertTrue(hasattr(user, 'profile'))  # Check if profile exists for user
        self.assertIsInstance(user.profile, Profile)  # Check if it's actually an instance of the Profile model
    


    def test_update_profile(self):
        """Test that a user can update their profile"""
        url = reverse('profile')
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'user_type': 'owner'  # Assuming user_type is included in the form
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()  # Refresh the user instance from the database to get the updated values
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')


class UserLoginTest(TestCase):

    def setUp(self):
        """Create a user for login tests"""
        self.user = get_user_model().objects.create_user(
            username='loginuser',
            email='loginuser@example.com',
            password='password123'
        )

    def test_user_login_valid(self):
        """Test that a user can log in with valid credentials"""
        url = reverse('login')
        data = {
            'username': 'loginuser',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('home'))  # Redirects to home on successful login

    def test_user_login_invalid(self):
        url = reverse('login')
        data = {
            'username': 'loginuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Please enter a correct username and password.")
    



class UserLogoutTest(TestCase):

    def setUp(self):
        """Create a user and log in for logout testing"""
        self.user = get_user_model().objects.create_user(
            username='logoutuser',
            email='logoutuser@example.com',
            password='password123'
        )
        self.client.login(username='logoutuser', password='password123')

    def test_user_logout(self):
        """Test that a user can log out successfully"""
        url = reverse('logout')  # Check the URL of the logout view
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'))  # After logging out, redirect to home
