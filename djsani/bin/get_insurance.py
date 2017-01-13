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

from djsani.insurance.models import StudentHealthInsurance
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE

from djzbar.utils.informix import get_session

from optparse import OptionParser

from datetime import datetime

"""
Grabs a student's health insurance profile
"""
EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
Accepts as input a student's college ID and
optional True/False for opting out of insurance
"""

parser = OptionParser(description=desc)
parser.add_option(
    "-i", "--ID",
    help="Student's college ID.",
    dest="cid"
)
parser.add_option(
    "-o", "--OPT_OUT",
    help="True or false.",
    dest="opt_out"
)

def main():
    """
    main function
    """

    print "Student's college ID = {}".format(cid)

    # create database session
    session = get_session(EARL)

    shi = session.query(StudentHealthInsurance).\
        filter_by(college_id=cid).first()

    print shi.__dict__

    # empty the table for opt_out
    if opt_out:
        session.query(StudentHealthInsurance).\
            filter_by(college_id=cid).\
            update(STUDENT_HEALTH_INSURANCE)

        session.commit()
        print shi.__dict__

    # test setting a date
    #dob = datetime.strptime("1974-12-03", "%Y-%m-%d")
    #shi.secondary_dob = dob
    #session.commit()
    #print shi.__dict__

    session.close()

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    cid = options.cid
    opt_out = options.opt_out

    mandatories = ['cid',]
    for m in mandatories:
        if not options.__dict__[m]:
            print "mandatory option is missing: %s\n" % m
            parser.print_help()
            exit(-1)

    sys.exit(main())
