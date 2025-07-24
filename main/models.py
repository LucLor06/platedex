from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from config import settings

class User(AbstractUser):
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def send_verification_email(self):
        if self.is_active:
            return
        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)
        link = reverse_lazy('accounts-email-verify-confirm', kwargs={'uidb64': uidb64, 'token': token})
        send_mail(
            subject='Verify Your Email',
            message=link,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email]
        )


class LicensePlate(models.Model):
    number = models.CharField(max_length=7, validators=[MinLengthValidator(2)])
    views = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.full_clean()
        return super().save(*args, **kwargs)


class LicensePlateSighting(models.Model):
    license_plate = models.ForeignKey('main.LicensePlate', related_name='sightings', on_delete=models.CASCADE)
    seen_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('main.User', related_name='sightings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} | {self.license_plate} | {self.seen_on}'