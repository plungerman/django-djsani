from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.medical_history.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='medical_history/success.html'
        ),
        name='medical_history_success'
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        'form', name="medical_history_form"
    ),
)
