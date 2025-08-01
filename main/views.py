from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegisterForm, EmailVerificationForm, SetPasswordForm, LicensePlateNumberForm, LicensePlateImageValidationForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import User, LicensePlate, LicensePlateSighting
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request: HttpRequest):
    if 'number' in request.GET:
        form = LicensePlateNumberForm(data=request.GET)
        if form.is_valid():
            plate_number = form.cleaned_data['number']
            return redirect(reverse('license-plates-detail', kwargs={'license_plate_number': plate_number}))
    return render(request, 'home.html')

def accounts_register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts-email-verify-done')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


class LoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')


class LogoutView(LogoutView):
    success_url = reverse_lazy('home')

def accounts_email_verify(request):
    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            form.send_verification_email()
            return redirect('accounts-email-verify-done')
    else:
        form = EmailVerificationForm()
    context = {'form': form}
    return render(request, 'accounts/email/verify.html', context)


def accounts_email_verify_done(request):
    return render(request, 'accounts/email/verify/done.html')

def accounts_email_verify_confirm(request, uidb64, token):
    context = {'already_verified': False, 'verification_success': False}

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if user.is_active:
            context['already_verified'] = True
        else:
            user.is_active = True
            user.save()
        context['verification_success'] = True

    return render(request, 'accounts/email/verify/confirm.html', context)


class AccountsPasswordResetView(PasswordResetView):
    template_name = 'accounts/password/reset.html'
    email_template_name = 'accounts/password/reset/emails/reset.txt'
    success_url = reverse_lazy('accounts-password-reset-done')


class AccountsPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password/reset/done.html'


class AccountsPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password/reset/confirm.html'
    post_reset_login = False
    success_url = reverse_lazy('accounts-password-reset-complete')
    form_class = SetPasswordForm


class AccountsPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password/reset/complete.html'

def license_plates_detail(request: HttpRequest, license_plate_number: str):
    license_plate, created = LicensePlate.objects.get_or_create(number__iexact=license_plate_number, defaults={'number': license_plate_number})
    if not created:
        license_plate.views += 1
        license_plate.save()
    context = {'license_plate': license_plate}
    return render(request, 'plates/detail.html', context)

@login_required
def sightings_create(request: HttpRequest, license_plate_number: str):
    license_plate, created = LicensePlate.objects.get_or_create(number__iexact=license_plate_number, defaults={'number': license_plate_number})
    license_plate_redirect = reverse('license-plates-detail', kwargs={'license_plate_number': license_plate.number})
    if request.method == "POST":
        form = LicensePlateImageValidationForm(instance=license_plate, data=request.POST, files=request.FILES)
        if form.is_valid():
            sighting = LicensePlateSighting.objects.create(user=request.user, license_plate=license_plate)
            messages.add_message(request, messages.SUCCESS, 'Congrats! Your sighting has been added.', extra_tags='modal')
            return redirect(license_plate_redirect)
    else:
        if LicensePlateSighting.objects.filter(user=request.user, license_plate=license_plate).exists():
            messages.add_message(request, messages.ERROR, 'You have already seen this plate!', extra_tags='modal')
            return redirect(license_plate_redirect)
        form = LicensePlateImageValidationForm()
    context = {'form': form, 'license_plate': license_plate}
    return render(request, 'plates/detail/sightings/add.html', context)

@login_required
def users_detail(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'users/detail.html', context)