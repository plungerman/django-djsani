from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('djsani.core.views',
    url(r'^admin/', include(admin.site.urls)),
    # auth
    url(
        r'^accounts/login',auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',auth_views.logout,
        {'next_page': reverse_lazy("auth_loggedout")},
        name="auth_logout"
    ),
    url(
        r'^accounts/loggedout',loggedout,
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
        r'^responsive/(?P<action>[-\w]+)',
        'responsive_switch', name="responsive_switch"
    ),
    # ajax post method to save various types characteristics to db and session
    url(
        r'^set-type/$', 'set_type', name="set_type"
    ),
    # home
    url(
        r'^$', 'home', name="home"
    ),
)
# authentication views
urlpatterns += patterns('djzbar.views.auth',
    # login required error page
    url(
        r'^login-required/@@UserID', 'login_required', name="login_required"
    ),
)
