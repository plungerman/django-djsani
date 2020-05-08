# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.views.generic import TemplateView
from djsani.dashboard import views


urlpatterns = [
    path(
        'success/',
        TemplateView.as_view(template_name='dashboard/success.html'),
        name='admin_success',
    ),
    # generic send mail functions
    path('send-mail/', views.sendmail, name='sendmail'),
    # ajax communication to paint the panels
    path('panels/', views.panels, name='dashboard_panels'),
    # ajax returns students because using home view is a
    # pain in the ass with security involved & spinner
    path('get-students/', views.get_students, name='get_students'),
    # simple ID search
    path('student/', views.student_detail, name='search_students'),
    # name search
    path('student/search/', views.advanced_search, name='search_advanced'),
    # student detail
    path('student/<int:cid>/', views.student_detail, name='student_detail'),
    # student detail content specific
    path(
        'student/<int:cid>/<str:medium>/<str:content_type>/',
        views.student_detail,
        name='student_detail_medium',
    ),
    # home
    path('', views.home, name='dashboard_home'),
]
