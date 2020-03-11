# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from djsani.medical_history import views


urlpatterns = [
    # waivers
    path('waivers/', include('djsani.medical_history.waivers.urls')),
    # medical history successfull submission redirect
    path(
        'success/',
        TemplateView.as_view(template_name='medical_history/success.html'),
        name='medical_history_success',
    ),
    # files upload form
    path('files/<str:name>/', views.file_upload, name='file_upload'),
    # medical history form: athletics or academics
    path(
        '<str:stype>/<str:display>/',
        views.index,
        name='medical_history_print',
    ),
    # medical history form: athletics or academics
    path('<str:stype>/', views.index, name='medical_history_form'),
]
