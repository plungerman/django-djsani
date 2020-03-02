# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path

from djmaidez.contact import views


urlpatterns = [
    path('form/', views.form, name='form'),
    path('populate/', views.populate, name='populate'),
    path('save/', views.save, name='save'),
    path('test/', views.test, name='test'),
]
