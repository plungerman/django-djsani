from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.dashboard.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='dashboard/success.html'
        ),
        name='admin_success'
    ),
    url(
        r'^student/(?P<cid>\d+)/$',
        'student_detail', name="student_detail"
    ),
    # home
    url(
        r'^$', 'home', name="dashboard_home"
    ),
)
