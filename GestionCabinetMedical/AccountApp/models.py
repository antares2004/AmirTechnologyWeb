from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone

def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("Birth date must be before today.")

class User(AbstractUser):
    pass
class specialty(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)],)
    specialties = models.ManyToManyField(specialty)

class Patient(User):
    national_id = models.CharField(
        max_length=8, unique=True,
        validators=[RegexValidator(r'^\d{8}$', "CIN must be exactly 8 digits.")],
    )
    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$', "Phone must be exactly 8 digits.")],
    )
    birth_date = models.DateField(validators=[validate_past_date])

