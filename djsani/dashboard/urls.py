from django.conf.urls import url
from django.views.generic import TemplateView

from djsani.dashboard import views

urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='dashboard/success.html'
        ),
        name='admin_success'
    ),
    # generic send mail functions
    url(
        r'^send-mail/$',
        views.sendmail, name="sendmail"
    ),
    # ajax communication to paint the panels
    url(
        r'^panels/$',
        views.panels, name="dashboard_panels"
    ),
    # ajax returns students because using home view is a
    # pain in the ass with security involved & spinner
    url(
        r'^get-students/$',
        views.get_students, name="get_students"
    ),
    # simple ID search
    url(
        r'^student/$',
        views.student_detail, name="student_search"
    ),
    # name search
    url(
        r'^student/search/$',
        views.advanced_search, name="advanced_search"
    ),
    # student detail
    url(
        r'^student/(?P<cid>\d+)/$',
        views.student_detail, name="student_detail"
    ),
    # student detail content specific
    url(
        r'^student/(?P<cid>\d+)/(?P<medium>[-\w]+)/(?P<content>[-\w]+)/$',
        views.student_detail,
        name="student_detail_medium"
    ),
    # home
    url(
        r'^$', views.home, name="dashboard_home"
    ),
]
