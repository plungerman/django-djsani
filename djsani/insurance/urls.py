from django.conf.urls import url
from django.views.generic import TemplateView

from djsani.insurance import views

urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='insurance/success.html'
        ),
        name='insurance_success'
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/(?P<cid>\d+)/$',
        views.form, name="insurance_form_dashboard"
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        views.form, name="insurance_form"
    ),
]
