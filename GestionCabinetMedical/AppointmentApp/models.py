from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    appointment_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey('AccountApp.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('AccountApp.Patient', on_delete=models.CASCADE)

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date',
            )
        ]

    def clean(self):
        # Only check when creating, or when the date has been changed
        if self.appointment_date:
            date_changed = True
            if self.pk:
                old = Appointment.objects.filter(pk=self.pk).values_list(
                    'appointment_date', flat=True).first()
                date_changed = old != self.appointment_date
            if date_changed and self.appointment_date <= timezone.now():
                raise ValidationError(
                    {'appointment_date': "The appointment date must be in the future."}
                )

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date:%Y-%m-%d %H:%M}"