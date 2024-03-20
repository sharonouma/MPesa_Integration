"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from mpesa_api.views import initiate_payment, mpesa_callback

from django.http import HttpResponse

from mpesa_api import views


# The 'admin' application is included by default in Django and provides a nice way of managing your site.
urlpatterns = [
     path('api/v1/access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('api/v1/online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('api/v1/callback', views.handle_callback, name='mpesa_callback'),  # Add this line for the callback URL
    # Other URL patterns go here if needed

    # register, confirmation, validation and callback urls
    # path('api/v1/c2b/register', views.register_urls, name="register_mpesa_validation"),
    # path('api/v1/c2b/confirmation', views.confirmation, name="confirmation"),
    # path('api/v1/c2b/validation', views.validation, name="validation"),
    # path('api/v1/c2b/callback', views.call_back, name="call_back"),
    # path('', views.home),  # Map the root URL to the home view
    # path('api/v1/', include('mpesa_api.urls')),
    # path('admin/', admin.site.urls),
    # path('sentry-debug/', trigger_error),
    # path('mpesa/initiate-payment/', initiate_payment, name='initiate-payment'),
    # path('mpesa/callback/', mpesa_callback, name='mpesa-callback'),
]
