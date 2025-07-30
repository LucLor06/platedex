from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User, LicensePlate
from django import forms
import easyocr
from django.core.exceptions import ValidationError
from .openai_api import license_plate_image_is_valid

reader = easyocr.Reader(['en'], gpu=False)

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

    def clean_number(self):
        data = self.cleaned_data['number']
        return data.upper()

class LicensePlateImageValidationForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = LicensePlate
        fields = ['image']

    def clean_image(self):
        data = self.cleaned_data['image'].read()
        ocr_output = reader.readtext(data, detail=0)
        if isinstance(ocr_output, list):
            ocr_output = ''.join(ocr_output)
        is_valid = license_plate_image_is_valid(self.instance, ocr_output)
        if not is_valid:
            raise ValidationError('The text in the image does not match the plate number. Ensure the picture is not too blurry, and does not contain any text in te background')
        return is_valid