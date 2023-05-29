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
from djauth.managers import LDAPManager
from djsani.core.models import Sport
from djsani.core.utils import get_manager


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

            if not user:
                username = row[1].split('@')
                if username[1] == 'carthage.edu':
                    # create a new user
                    eldap = LDAPManager()
                    result_data = eldap.search(username[0], field='cn')
                    if result_data:
                        groups = eldap.get_groups(result_data)
                        #print(cid, groups)
                        #user = eldap.dj_create(result_data, groups=groups)
                    else:
                        print("No user found with username: {0}".format(username))
                else:
                    print("{0} is not a carthage email address.".format(row[1]))

            if user:
                print(user)

            '''
                manager = get_manager(cid)
                if manager:
                    manager.athlete=True
                    manager.save()
                    manager.sports.add(sport)
            '''


if __name__ == '__main__':
    args = parser.parse_args()
    code = args.code
    test = args.test

    sys.exit(main())
