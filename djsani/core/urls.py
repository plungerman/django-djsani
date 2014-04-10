from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('djsani.core.views',
    # my app
    url(
        r'^insurance/', include("djsani.insurance.urls")
    ),
    url(
        r'^$', 'home', name="home"
    ),
)
