from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.admin.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='admin/success.html'
        ),
        name='admin_success'
    ),
    # home
    url(
        r'^$', 'home', name="home"
    ),
)
