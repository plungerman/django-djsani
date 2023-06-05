# -*- coding: utf-8 -*-

import argparse
import django
import os
import sys

django.setup()

from django.conf import settings
from djsani.medical_history.waivers.models import Meni
from djsani.medical_history.waivers.models import Privacy
from djsani.medical_history.waivers.models import Reporting
from djsani.medical_history.waivers.models import Risk
from djsani.medical_history.waivers.models import Sicklecell
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import StudentMedicalManager
from djsani.core.views import BASES


# set up command-line options
desc = """
Accepts as input database table name related to medical forms:

python find_dupes.py --table=student_meni_waiver
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-t", "--table",
    required=True,
    help="Database table",
    dest="table",
)


def main():
    """main function."""
    model = BASES[table]
    print("select all managers")
    managers = StudentMedicalManager.objects.filter(created_at__gte=settings.START_DATE)
    for man in managers:
        try:
            obj = model.objects.filter(user=man.user).filter(created_at__gte=settings.START_DATE)
            if len(obj) > 1:
                print("Manager ID {0} has more than 1 rec: {1}".format(
                    man.user.id, len(obj),
                ))
        except Exception as error:
            print(error)


if __name__ == '__main__':
    args = parser.parse_args()
    table = args.table
    sys.exit(main())
