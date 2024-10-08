# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from djauth.views import loggedout
from djsani.core import views


admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = [
    # sign in as user
    path('rocinante/', include('loginas.urls')),
    # django admin
    path('rocinante/', admin.site.urls),
    # we don't want users created through django admin
    path(
        'rocinante/auth/user/add/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    # saml2 auth
    path('saml/', include('django_saml.urls')),
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # admin manager
    path('dashboard/', include('djsani.dashboard.urls')),
    # insurance forms
    path('insurance/', include('djsani.insurance.urls')),
    # medical history
    path('history/', include('djsani.medical_history.urls')),
    # override mobile first responsive UI
    path(
        'responsive/<str:action>/',
        views.responsive_switch,
        name='responsive_switch',
    ),
    # ajax post method to save various types characteristics to db and session
    path('set-val/', views.set_val, name='set_val'),
    # ajax post method to rotate an image 90 degress clockwise
    path('rotate-photo/', views.rotate_photo, name='rotate_photo'),
    # home
    path('', views.home, name='home'),
]
