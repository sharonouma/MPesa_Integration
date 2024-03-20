from django.urls import path

from . import views

# URL pattern for getting M-Pesa access token
urlpatterns = [
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('callback', views.handle_callback, name='mpesa_callback'),  # Add this line for the callback URL
    # Other URL patterns go here if needed

    # register, confirmation, validation and callback urls
    # path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    # path('c2b/confirmation', views.confirmation, name="confirmation"),
    # path('c2b/validation', views.validation, name="validation"),
    # path('c2b/callback', views.call_back, name="call_back"),

]
