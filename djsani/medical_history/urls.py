from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.medical_history.views',
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
    # medical history form: athletics or academics
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/(?P<display>[a-zA-Z0-9_-]+)/$',
        'form', name="medical_history_print"
    ),
    # medical history form: athletics or academics
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        'form', name="medical_history_form"
    ),
)
