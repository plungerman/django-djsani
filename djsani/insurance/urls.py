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
        r'^',
        'insurance_form', name="insurance_form"
    ),
)
