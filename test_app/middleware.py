# middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils import timezone


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not (request.path_info == reverse('login') or request.path_info == reverse('register')):
            return redirect(reverse('login'))

        response = self.get_response(request)
        return response

