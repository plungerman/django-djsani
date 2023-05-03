# -*- coding: utf-8 -*-

from django.contrib import admin
from djsani.core.models import StudentProfile



class StudentProfileAdmin(admin.ModelAdmin):
    """Data model class for student profiles."""

    list_display  = (
        'last_name',
        'first_name',
        'residency',
        'username',
        'cid',
        #'address1',
        #'address2',
        #'city',
        #'state',
        #'postal_code',
    )
    search_fields = (
        'user__last_name',
        'user__username',
        'user__id',
        'phone',
        'city',
        'state',
        'postal_code',
    )
    list_filter = ('residency',)
    list_max_show_all = 500
    list_per_page = 500
    save_on_top = True
    ordering = ['user__last_name']


admin.site.register(StudentProfile, StudentProfileAdmin)
