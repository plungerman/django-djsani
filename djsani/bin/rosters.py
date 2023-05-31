# -*- coding: utf-8 -*-

"""Load roster data for sport."""

import argparse
import csv
import django
import os
import sys

django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')

from django.conf import settings
from django.contrib.auth.models import User
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager


# set up command-line options
desc = """
    Accepts as input the 4 letter code for the sport. e.g. wscr
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-c',
    '--code',
    required=True,
    help="Sport code",
    dest='code',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Obtain all the data from a database table."""
    phile = os.path.join(settings.BASE_DIR, 'rosters/{0}.csv'.format(code))
    try:
        sport = Sport.objects.get(code=code.upper())
    except Exception:
        print("Invalid sport code: {0}".format(code))
        sys.exit(-1)

    with open(phile) as roster:
        reader = csv.reader(roster, delimiter='|')
        for row in reader:
            cid=row[0]
            try:
                user = User.objects.get(pk=cid)
            except User.DoesNotExist:
                user = None

            if user:
                try:
                    manager = StudentMedicalManager.objects.filter(
                        user=user,
                        created_at__gte=settings.START_DATE,
                    ).first()
                except Exception as error:
                    print('error:')
                    print(error)
                    manager = None
                if manager:
                    manager.athlete=True
                    manager.save()
                    manager.sports.add(sport)
                else:
                    print(user.id)
                    print('no manager found')


if __name__ == '__main__':
    args = parser.parse_args()
    code = args.code
    test = args.test

    sys.exit(main())
