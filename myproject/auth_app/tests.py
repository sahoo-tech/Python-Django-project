from django.test import TestCase, Client
from .models import CustomUser, PatientProfile, DoctorProfile


class AuthenticationTests(TestCase):
    """Test authentication system."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_home_page_loads(self):
        """Test home page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        """Test signup page loads."""
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        """Test login page loads."""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_patient_signup(self):
        """Test patient signup."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password1': 'SecurePass123',
            'password2': 'SecurePass123',
            'user_type': 'patient',
            'address_line1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'pincode': '10001',
        }
        response = self.client.post('/signup/', data)
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.first()
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.user_type, 'patient')

    def test_patient_login(self):
        """Test patient login."""
        # Create user
        user = CustomUser.objects.create_user(
            email='patient@example.com',
            username='patient',
            password='TestPass123',
            user_type='patient'
        )
        PatientProfile.objects.create(user=user)

        # Login
        login_data = {
            'email': 'patient@example.com',
            'password': 'TestPass123',
        }
        response = self.client.post('/login/', login_data)
        self.assertEqual(response.status_code, 302)
