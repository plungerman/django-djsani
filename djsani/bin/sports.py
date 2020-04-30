# -*- coding: utf-8 -*-

import csv
import os
import sys
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')

# required if using django models
import django
django.setup()

from django.conf import settings
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.models import SPORTS

import argparse
import logging

logger = logging.getLogger('debug_logfile')

# set up command-line options
desc = """
  Accepts as input a college ID
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    '-i', '--cid',
    help="College ID",
    dest='cid',
    required=False,
)
parser.add_argument(
    '-f', '--file',
    help="File name",
    dest='phile',
    required=False,
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)

PHILE = os.path.join(settings.BASE_DIR, 'sql/sports.sql')


def _xsql(cid):
    """Private function for executing the SQL incantation."""
    with open(PHILE) as incantation:
        sql = '{0}{1}'.format(incantation.read(), cid)
    if test:
        print('sql incantation:')
        print(sql)
    else:
        logger.debug("sql = {}".format(sql))
    with get_connection() as connection:
        row = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchall()
        return row


def main():
    """Obtain the sports in which a student participates."""
    if cid:
        print(_xsql(cid))
    else:
        sendero = os.path.join(settings.BASE_DIR, 'sql', phile)
        if os.path.isfile(sendero):
            with open(sendero, 'r') as csv_file:
                reader = csv.DictReader(csv_file, delimiter='|')
                for row in reader:
                    sports = []
                    clubsorgs = _xsql(row['ID'])
                    for sport in row['Sports'].split(','):
                        for s in SPORTS:
                            if s[0] == sport:
                                sports.append(s[1])
                    print(row['ID'], row['Athlete Status'], clubsorgs, sports)
        else:
            print("{0} is not a valid file".format(phile))


if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    phile = args.phile
    test = args.test
    if not cid and not phile:
        print("You must provide a college ID or a file name")
        sys.exit()

    if test:
        print(args)

    sys.exit(main())
