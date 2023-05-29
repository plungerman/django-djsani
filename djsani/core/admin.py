# -*- coding: utf-8 -*-

from django.contrib import admin
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager
from djsani.core.models import CoachProfile
from djsani.core.models import StudentProfile


class SportAdmin(admin.ModelAdmin):
    """Data model class for sports."""

    list_display  = (
        'name',
        'code',
        'status',
    )
    search_fields = ('name', 'code')


class StudentMedicalManagerAdmin(admin.ModelAdmin):
    """Data model class for student medical manager."""

    list_display  = (
        'user',
        'id',
        'athlete',
        'created_at',
    )
    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__username',
        'user__id',
    )
    raw_id_fields = ['user']
    list_filter = ['athlete']


class CoachProfileAdmin(admin.ModelAdmin):
    """Data model class for student profiles."""

    list_display  = (
        'last_name',
        'first_name',
        'get_sports',
        'username',
        'cid',
    )
    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__username',
        'user__id',
    )
    list_max_show_all = 500
    list_per_page = 500
    save_on_top = True
    ordering = ['user__last_name']
    raw_id_fields = ['user']


class StudentProfileAdmin(admin.ModelAdmin):
    """Data model class for student profiles."""

    list_display  = (
        'last_name',
        'first_name',
        'class_year',
        'residency',
        'username',
        'cid',
        'created_at',
    )
    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__username',
        'user__id',
        'phone',
        'city',
        'state',
        'postal_code',
    )
    list_filter = ['residency']
    list_max_show_all = 500
    list_per_page = 500
    save_on_top = True
    ordering = ['user__last_name']
    raw_id_fields = ['user']


admin.site.register(CoachProfile, CoachProfileAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(StudentMedicalManager, StudentMedicalManagerAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
