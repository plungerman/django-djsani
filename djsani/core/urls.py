from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from djsani.core import views

from djauth.views import loggedout
from djzbar.views import auth

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = [
    # we don't want users created through django admin
    url(
        r'^admin/auth/user/add/$',
        RedirectView.as_view(url=reverse_lazy("auth_login"))
    ),
    url(r'^admin/', include(admin.site.urls)),
    # auth
    url(
        r'^accounts/login/$',auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',auth_views.logout,
        {'next_page': reverse_lazy("auth_loggedout")},
        name="auth_logout"
    ),
    url(
        r'^accounts/loggedout/$', loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name="auth_loggedout"
    ),
    url(
        r'^accounts/$',
        RedirectView.as_view(url=reverse_lazy("auth_login"))
    ),
    # admin manager
    url(
        r'^dashboard/', include("djsani.dashboard.urls")
    ),
    # insurance forms
    url(
        r'^insurance/', include("djsani.insurance.urls")
    ),
    # medical history
    url(
        r'^history/', include("djsani.medical_history.urls")
    ),
    # override mobile first responsive UI
    url(
        r'^responsive/(?P<action>[-\w]+)/',
        views.responsive_switch, name="responsive_switch"
    ),
    # ajax post method to save various types characteristics to db and session
    url(
        r'^set-val/$', views.set_val, name="set_val"
    ),
    # ajax post method to rotate an image 90 degress clockwise
    url(
        r'^rotate-photo/$', views.rotate_photo, name="rotate_photo"
    ),
    # home
    url(
        r'^$', views.home, name="home"
    ),
    # authentication views
    # login required error page
    url(
        r'^login-required/?cid=@@UserID', auth.login_required, name="login_required"
    ),
]
