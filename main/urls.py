from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.accounts_register, name='accounts-register'),
    path('accounts/email/verify/', views.accounts_email_verify, name='accounts-email-verify'),
    path('accounts/email/verify/done/', views.accounts_email_verify_done, name='accounts-email-verify-done'),
    path('accounts/email/verify/<uidb64>/<token>/', views.accounts_email_verify_confirm, name='accounts-email-verify-confirm'),
    path('accounts/password/reset/', views.AccountsPasswordResetView.as_view(), name='accounts-password-reset'),
    path('accounts/password/reset/done/', views.AccountsPasswordResetDoneView.as_view(), name='accounts-password-reset-done'),
    path('accounts/password/reset/confirm/', views.AccountsPasswordResetConfirmView.as_view(), name='accounts-password-reset-confirm'),
]