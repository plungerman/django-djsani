from django.conf.urls import include, url
from django.views.generic import TemplateView

from djsani.medical_history import views

urlpatterns = [
    # waivers
    url(
        r'^waivers/', include("djsani.medical_history.waivers.urls")
    ),
    # medical history successfull submission redirect
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='medical_history/success.html'
        ),
        name='medical_history_success'
    ),
    # files upload form
    url(
        r'^files/(?P<name>[a-zA-Z0-9_-]+)/$',
        views.file_upload, name="file_upload"
    ),
    # medical history form: athletics or academics
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/(?P<display>[a-zA-Z0-9_-]+)/$',
        views.history, name="medical_history_print"
    ),
    # medical history form: athletics or academics
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        views.history, name="medical_history_form"
    ),
]
