from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_date', 'doctor', 'patient', 'status', 'duration_minutes')
    list_filter = ('status', 'doctor', 'appointment_date')
    search_fields = ('doctor__last_name', 'patient__last_name', 'patient__national_id', 'reason')
    ordering = ('appointment_date',)