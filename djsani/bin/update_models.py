# -*- coding: utf-8 -*-

"""Test for the set_val() view."""

import argparse
import django
import os
import sys
django.setup()
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')

from djsani.core.models import StudentMedicalManager
from djsani.core.views import BASES
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Meni
from djsani.medical_history.waivers.models import Privacy
from djsani.medical_history.waivers.models import Reporting
from djsani.medical_history.waivers.models import Risk
from djsani.medical_history.waivers.models import Sicklecell


# set up command-line options
desc = """
    Accepts as input a database table name
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-t',
    '--table',
    required=True,
    help="Database table",
    dest='table',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Obtain all the data from a database table."""
    try:
        model = BASES[table]
    except Exception:
        print("Invalid table name: {0}".format(table))
        sys.exit()

    rows = model.objects.using('informix').all().order_by('id')
    print("select all from table: {0}".format(table))
    for row in rows:
        print(row.__dict__)


if __name__ == '__main__':
    args = parser.parse_args()
    table = args.table
    test = args.test

    sys.exit(main())
