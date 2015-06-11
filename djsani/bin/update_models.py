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

from djsani.medical_history.waivers.models import Meni, Privacy, Reporting
from djsani.medical_history.waivers.models import Risk, Sicklecell
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import StudentMedicalManager
from djsani.core.views import BASES

from djzbar.utils.informix import get_session

from sqlalchemy import exc

import argparse

"""
"""

from djzbar.settings import INFORMIX_EARL_PROD as EARL
#EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
Accepts as input a student's college ID
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-t", "--table",
    help="Database table",
    dest="table"
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)

def main():
    """
    main function
    """

    # create database session
    session = get_session(EARL)
    print EARL
    model = BASES[table]

    objects = session.query(model).order_by(model.id).all()
    count = 1
    error = False
    print "select all from table: {}".format(table)
    for obj in objects:
        if test:
            try:
                manager = session.query(StudentMedicalManager).\
                    filter_by(college_id=obj.college_id).one()
                count += 1
            except:
                #pass
                print "Error on manager with ID: {}".format(obj.college_id)
        else:
            try:
                manager = session.query(StudentMedicalManager).\
                    filter_by(college_id=obj.college_id).one()
                obj.manager_id = manager.id
                count += 1
            except exc.SQLAlchemyError as e:
                print e
                print obj
                print count
                error = True
                session.rollback()
                pass

    print count

    if not error and not test:
        session.commit()

    session.close()

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    table = args.table
    test = args.test

    if not table:
        print "mandatory option is missing: table name\n"
        parser.print_help()
        exit(-1)
    sys.exit(main())
