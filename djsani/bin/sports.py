# -*- coding: utf-8 -*-

import argparse
import csv
import logging
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
    required=True,
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)

PHILE = os.path.join(settings.BASE_DIR, 'sql/sports_student.sql')


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
    print(_xsql(cid))


if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    test = args.test
    if test:
        print(args)
    sys.exit(main())
