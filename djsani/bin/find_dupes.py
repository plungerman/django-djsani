# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings')

import django
django.setup()

from django.conf import settings

from djsani.medical_history.waivers.models import Meni, Privacy, Reporting
from djsani.medical_history.waivers.models import Risk, Sicklecell
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import StudentMedicalManager
from djsani.core.views import BASES

from djzbar.utils.informix import get_session

import argparse


EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
Accepts as input database table name related to medical forms:

python find_dupes.py --table=cc_student_meni_waiver
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-t", "--table",
    required=True,
    help="Database table",
    dest="table"
)

def main():
    """
    main function
    """

    # create database session
    session = get_session(EARL)

    model = BASES[table]

    print("select all managers")
    managers = session.query(StudentMedicalManager).all()
    for man in managers:
        try:
            obj = session.query(model).filter_by(college_id=man.college_id).all()
            if len(obj) > 1:
                print("Manager ID {} has more than 1 rec: {}".format(
                    man.college_id, len(obj)
                ))
        except:
            pass

    session.commit()
    session.close()

######################
# shell command line
######################

if __name__ == '__main__':

    args = parser.parse_args()
    table = args.table

    sys.exit(main())
