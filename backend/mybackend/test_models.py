import json
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from mybackend.mongoDB import MongoDBClient
from django.contrib.auth.models import User  # Replace with your User model
from mybackend.authenticate_request import authenticate_request  # Import your decorator
from django.urls import reverse
import jwt

# Your MongoDBClient for users
user = MongoDBClient('mongodb+srv://Admin:1234@mlproject.obivlrq.mongodb.net/?retryWrites=true&w=majority', "E-commerce", "User")

# Secret key for JWT token
JWT_SECRET_KEY = 'ML_Project'  # Replace with your actual secret key

def generate_token(username):
    payload = {
        'username': username,
        # You can add more claims to the payload if needed
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

class AuthenticateRequestDecoratorTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user =  user.find_one({"username":"mark","password":"a"})

        # Create a test request factory
        self.factory = RequestFactory()

    def test_authenticated_request(self):
        # Create an authenticated request with a valid JWT token
        token = generate_token(self.user['username'])
        request = self.factory.post(reverse('product_normal'), data={}, content_type='application/json', HTTP_AUTHORIZATION=f'Token {token}')

        # Apply the decorator to the view
        decorated_view = authenticate_request(self.dummy_view)
        response = decorated_view(request)

        # Check that the view was called and returned a response
        self.assertEqual(response.status_code, 200)

     # Define a dummy view for testing
    def dummy_view(self, request):
        return JsonResponse({'status': 'success'})

    # Define a view that raises an exception for testing
    def view_with_exception(self, request):
        raise Exception('An error occurred')

    


