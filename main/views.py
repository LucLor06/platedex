from django.shortcuts import render
from django.http import HttpRequest
from .forms import RegisterForm
from django.shortcuts import redirect

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