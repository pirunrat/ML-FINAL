def authenticate_token(request):
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return False
    if auth_token == "YOUR_SECRET_TOKEN":
        return True
    return False