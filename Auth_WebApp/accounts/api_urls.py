# d:\Auth_WebApp\Auth_WebApp\accounts\api_urls.py
from django.urls import path
from .views import (
    RegisterAPI, 
    LoginAPI, 
    LogoutAPI, 
    RequestPasswordResetOTPAPI, 
    ResetPasswordWithOTPAPI, 
    DownloadUserCSVAPI, 
    DownloadUserPDFAPI
)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='api_register'),
    path('login/', LoginAPI.as_view(), name='api_login'),
    path('logout/', LogoutAPI.as_view(), name='api_logout'),
    
    # Password Reset
    path('password-reset/request/', RequestPasswordResetOTPAPI.as_view(), name='api_request_otp'),
    path('password-reset/confirm/', ResetPasswordWithOTPAPI.as_view(), name='api_confirm_otp'),

    # Data Export
    path('download/csv/', DownloadUserCSVAPI.as_view(), name='api_download_csv'),
    path('download/pdf/', DownloadUserPDFAPI.as_view(), name='api_download_pdf'),
]
