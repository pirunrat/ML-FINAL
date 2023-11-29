import json
from django.http import JsonResponse
from .mongoDB import MongoDBClient
from django.contrib.auth import authenticate
import jwt  # You may need to install the `PyJWT` package

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

def authenticate_request(function):
    def wrapper(request, *args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.headers.get('Authorization'):  # Check if the user is authenticated
                print(request.headers.get('Authorization'))
                return function(request, *args, **kwargs)
            else:
                print("I'm here")
                try:
                    data = json.loads(request.body.decode('utf-8'))

                    username = data['username']
                    password = data['password']

                    query = user.find_one({"username":username,"password":password})

                   
                    if query is not None:
                        # Authentication successful, generate a token
                        token = generate_token(username)
                        response = JsonResponse({'token': token}, status=200)
                        
                        return response
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Authentication failed.'}, status=401)
                except json.JSONDecodeError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
                except Exception as error:
                    return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(error)}'}, status=500)
        else:
            # Handle unauthenticated GET requests or other HTTP methods
            return function(request, *args, **kwargs)
    return wrapper
