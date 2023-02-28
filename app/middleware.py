from django.shortcuts import render
from django.contrib.sessions.middleware import SessionMiddleware

#
# class ExceptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         return response
#
#     def process_exception(self, request):
#         return render(request, 'app/error.html')
#
#
# class LogoutMiddleware(SessionMiddleware):
#     def process_request(self, request):
#         request.session.set_expiry(10)
