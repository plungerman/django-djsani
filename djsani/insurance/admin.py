# -*- coding: utf-8 -*-

from django.contrib import admin
from djsani.insurance.models import StudentHealthInsurance


class StudentHealthInsuranceAdmin(admin.ModelAdmin):
    """Data model class for student health insurance."""

    raw_id_fields = ('user', 'manager')
    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__username',
        'user__id',
    )


admin.site.register(StudentHealthInsurance, StudentHealthInsuranceAdmin)
