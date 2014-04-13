from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('djsani.core.views',
    # insurance forms
    url(
        r'^insurance/', include("djsani.insurance.urls")
    ),
    # medical history
    url(
        r'^medical-history/', include("djsani.medical_history.urls")
    ),
    url(
        r'^set-student-type/$', 'set_student_type', name="set_student_type"
    ),
    url(
        r'^$', 'home', name="home"
    ),
)
