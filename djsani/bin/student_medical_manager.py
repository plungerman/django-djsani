# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from django.conf import settings

from djsani.core.models import StudentMedicalManager
from djzbar.utils.informix import get_session

from optparse import OptionParser


"""
Grabs a student's medical manager or creates one if absent
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

    # create database session
    session = get_session(EARL)

    manager = session.query(StudentMedicalManager).\
        filter_by(college_id=cid).\
        filter(StudentMedicalManager.current(settings.START_DATE)).first()

    if not manager:
        # see if we have a past manager with immunization set
        immunization = False
        obj = session.query(StudentMedicalManager).filter_by(college_id=cid).\
            filter_by(cc_student_immunization=1).first()
        if obj:
            immunization = True
        # create new manager
        manager = StudentMedicalManager(
            college_id=cid, cc_student_immunization=immunization
        )

        session.add(manager)
        session.commit()

    print "entire object as dictionary:\n"
    print manager.__dict__

    for m in manager:
        if m.current:
            print m.__dict__
        else:
            print m.created_at, m.current

    session.close()

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
