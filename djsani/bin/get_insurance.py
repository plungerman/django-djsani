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

from djsani.insurance.models import StudentHealthInsurance

from djzbar.settings import INFORMIX_EARL_TEST as INFORMIX_EARL

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine

from optparse import OptionParser

"""
Grabs a student's health insurance profile
"""

# set up command-line options
desc = """
Accepts as input a student's college ID
"""

parser = OptionParser(description=desc)
parser.add_option(
    "-i", "--ID",
    help="Studnet's college ID.",
    dest="cid"
)

def main():
    """
    main function
    """

    print "Student's college ID = {}".format(cid)

    engine = create_engine(INFORMIX_EARL, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    session = Session()
    shi = session.query(StudentHealthInsurance).filter_by(college_id=cid).first()

    print shi.__dict__

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
