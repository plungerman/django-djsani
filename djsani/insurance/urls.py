from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.insurance.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='insurance/success.html'
        ),
        name='insurance_success'
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/(?P<cid>\d+)/$',
        'form', name="insurance_form_dashboard"
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        'form', name="insurance_form"
    ),
)
