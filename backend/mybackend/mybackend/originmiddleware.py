from django.http import JsonResponse

ALLOWED_ORIGINS = ["http://localhost:3000"]

class OriginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get('Origin')

        try:
            if origin not in ALLOWED_ORIGINS:
                return JsonResponse({'error':'Unauthorized Origin'},status=403)
            else:
                response = self.get_response(request)
                return response
        except Exception as error:
            print(f"An error occurs {error}")