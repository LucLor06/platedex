from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.accounts_register, name='accounts-register'),
    path('accounts/email/verify/done/', views.accounts_email_verify_done, name='accounts-email-verify-done')
]