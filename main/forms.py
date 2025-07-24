from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Minimum 8 characters. Must include letters and numbers.'

    def save(self, commit=True):
        if commit:
            self.instance.send_verification_email()
        return super().save(commit)