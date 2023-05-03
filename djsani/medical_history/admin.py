# -*- coding: utf-8 -*-

from django.contrib import admin
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory


class AthleteMedicalHistoryAdmin(admin.ModelAdmin):
    """Data model class for athlete medical history."""

    raw_id_fields = ('user', 'manager')


class StudentMedicalHistoryAdmin(admin.ModelAdmin):
    """Data model class for student medical history."""

    raw_id_fields = ('user', 'manager')

admin.site.register(AthleteMedicalHistory, AthleteMedicalHistoryAdmin)
admin.site.register(StudentMedicalHistory, StudentMedicalHistoryAdmin)

