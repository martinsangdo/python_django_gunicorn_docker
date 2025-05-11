#This is used to apply Authentication/Authorization/... with JWT, ... (later) for all APIs that have prefix "/api/"
from django.http import HttpResponse

class APIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request BEFORE the view (controller) is called
        #if request.path.startswith('/api/'):
            #print(f"API Middleware processing request to: {request.path}")
            # You can perform actions here, e.g., authentication, logging, etc.

        response = self.get_response(request)

        # Code to be executed for each request/response AFTER the view is called
        #if request.path.startswith('/api/'):
            #print(f"API Middleware processing response for: {request.path}")
            # You can perform actions here, e.g., modify headers, log response, etc.

        return response