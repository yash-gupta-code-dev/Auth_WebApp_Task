from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', TemplateView.as_view(template_name="account/login.html"), name='account_login'),
    path('signup/', TemplateView.as_view(template_name="account/signup.html"), name='account_signup'),
    path('dashboard/', TemplateView.as_view(template_name="account/dashboard.html"), name='account_dashboard'),
    path('password/reset/', TemplateView.as_view(template_name="account/password_reset_otp.html"), name='account_reset_password'),
]

from .views import RegisterAPI, LoginAPI, LogoutAPI, RequestPasswordResetOTPAPI, ResetPasswordWithOTPAPI, DownloadUserCSVAPI, DownloadUserPDFAPI

urlpatterns += [
    path('register/', RegisterAPI.as_view(), name='api_register'),
    path('login/', LoginAPI.as_view(), name='api_login'),
    path('logout/', LogoutAPI.as_view(), name='api_logout'),
    
    #OTP URLs
    path('password-reset/request/', RequestPasswordResetOTPAPI.as_view(), name='api_request_otp'),
    path('password-reset/confirm/', ResetPasswordWithOTPAPI.as_view(), name='api_confirm_otp'),
]