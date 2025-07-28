from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User, LicensePlate
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Minimum 8 characters. Must include letters and numbers.'

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.send_verification_email()


class EmailVerificationForm(forms.Form):
    email = forms.EmailField()

    def send_verification_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email__iexact=email)
            user.send_verification_email()
        except User.DoesNotExist:
            pass

    
class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = 'Minimum 8 characters. Must include letters and numbers.'
        

class LicensePlateNumberForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        fields = ['number']