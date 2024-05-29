# -*- coding: utf-8 -*-

"""Load roster data for sport."""

import argparse
import django
import os
import requests
import sys

django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')

from django.conf import settings
from django.contrib.auth.models import User
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager
from urllib3.util import Retry

# set up command-line options
desc = "Accepts as input --test for debugging."
parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Obtain all the data from the API and insert into database."""
    session = requests.Session()
    retries = Retry(
        total=settings.WORKDAY_REQUESTS_RETRY,
        backoff_factor=0.1,
        status_forcelist=[502, 503, 504],
        allowed_methods={'GET'},
    )
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))
    response = session.get(
        settings.WORKDAY_SPORTS_ROSTERS,
        auth=(settings.WORKDAY_USERNAME, settings.WORKDAY_PASSWORD),
    )
    if response:
        jason = response.json()
        for athlete in jason['Report_Entry']:
            code = athlete['referenceID']
            try:
                sport = Sport.objects.get(code=code.upper())
            except Exception:
                print("Invalid sport code: {0}".format(code))
                sport = None
            if sport:
                cid=athlete['Student_ID']
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
    test = args.test
    sys.exit(main())
