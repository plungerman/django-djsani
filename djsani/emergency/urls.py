from django.conf.urls import url

from djmaidez.contact import views


urlpatterns = [
    url(r'^form/$', views.form, name='form'),
    url(r'^populate/$', views.populate, name='populate'),
    url(r'^save/$', views.save, name='save'),
    url(r'^test/$', views.test, name='test')
]
