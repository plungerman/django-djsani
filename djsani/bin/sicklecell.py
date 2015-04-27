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

import django

django.setup()

from django.conf import settings
from djsani.core.utils import get_manager
from djsani.medical_history.waivers.models import Sicklecell
from djzbar.utils.informix import get_session

from optparse import OptionParser

"""
Grabs an athlete's sicklecell waiver
"""

EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
Accepts as input a student's college ID
"""

parser = OptionParser(description=desc)
parser.add_option(
    "-i", "--ID",
    help="Student's college ID.",
    dest="cid"
)

def main():
    """
    main function
    """

    print "Student's college ID = {}".format(cid)
    session = get_session(settings.INFORMIX_EARL)

    student = session.query(Sicklecell).\
        filter_by(college_id=cid).filter(\
            (Sicklecell.proof == 1) | \
            (Sicklecell.created_at > settings.START_DATE)\
        ).first()

    print student.__dict__

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    cid = options.cid

    mandatories = ['cid',]
    for m in mandatories:
        if not options.__dict__[m]:
            print "mandatory option is missing: %s\n" % m
            parser.print_help()
            exit(-1)

    sys.exit(main())
