from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    email = models.EmailField()

    REQUIRED_FIELDS = ['email']


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