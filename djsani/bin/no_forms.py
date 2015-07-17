# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from django.conf import settings
from djzbar.utils.informix import do_sql


# set up command-line options
desc = """
    Find current students who have not submitted medical forms.
"""

def main():
    """
    main method
    """
    txt = "{}/data/sql/no_medical_forms.sql".format(settings.ROOT_DIR)
    print txt
    f = open (txt,"r")
    sequel = f.read()
    """
    print sequel
    print settings.INFORMIX_DEBUG
    print settings.INFORMIX_EARL
    """
    objs = do_sql(sequel,key=settings.INFORMIX_DEBUG,earl=settings.INFORMIX_EARL)
    for o in objs:
        print "{} {}<{}@carthage.edu>,".format(
            o.firstname, o.lastname, o.ldap_name
        )
    f.close()

######################
# shell command line
######################

if __name__ == "__main__":

    sys.exit(main())
