from django.contrib.auth.forms import UserCreationForm
from .models import User
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

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email__iexact=email)
            user.send_verification_email()
        except User.DoesNotExist:
            pass