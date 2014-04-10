django-djsani
==============

Django apps for the Health and Counseling Centre

# Apache Configuration

    # Health & Counceling apps
    <Location /campus-life/health-counseling/forms>
    WSGIProcessGroup djsani
    WSGIApplicationGroup djsani
    </Location>
    WSGIDaemonProcess djsani user=www-data group=www-data processes=1 threads=5
    WSGIImportScript /d2/django_projects/djsani/wsgi process-group=djsani application-group=djsani
    WSGIScriptAlias /campus-life/health-counseling/forms "/data2/django_projects/djsani/wsgi.py"

