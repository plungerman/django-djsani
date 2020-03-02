# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.views.generic import TemplateView
from djsani.insurance import views


urlpatterns = [
    path(
        'success/',
        TemplateView.as_view(template_name='insurance/success.html'),
        name='insurance_success',
    ),
    path('<str:stype>/<int:cid>/', views.form, name='insurance_form_dashboard'),
    path('<str:stype>/', views.form, name='insurance_form'),
]
