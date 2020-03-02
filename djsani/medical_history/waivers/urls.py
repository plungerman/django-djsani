# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from djsani.medical_history.waivers import views


urlpatterns = [
    # generic waiver successfull submission redirect
    path(
        'success/',
        TemplateView.as_view(
            template_name='medical_history/waivers/success.html',
        ),
        name='waiver_success',
    ),
    # medical history waiver forms
    path('<str:stype>/<str:wtype>/', views.form, name='waiver_form'),
    path('', RedirectView.as_view(url=reverse_lazy('home'))),
]
