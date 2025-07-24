from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegisterForm
from django.shortcuts import redirect
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

def home(request: HttpRequest):
    return render(request, 'home.html')

def accounts_register(request:HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts-email-verify-done')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

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
