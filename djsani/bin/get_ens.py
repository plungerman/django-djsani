#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import argparse

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.11/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from djmaidez.core.models import ENS_CODES, ENS_FIELDS
from djzbar.utils.informix import do_sql

"""
Fetch emergency contact information from database
"""

# set up command-line options
desc = """
Accepts as input a college ID
"""


parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    "-c", "--cid",
    required=True,
    help="Please provide a college ID.",
    dest='cid'
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)


def main():
    """
    main method
    """

    for c in ENS_CODES:
        print("++{}++++++++++++++++++++++".format(c))
        sql = 'SELECT * FROM aa_rec WHERE aa = "{}" AND id="{}"'.format(c,cid)

        if test:
            print("SQL\n{}".format(sql))

        result = do_sql(sql, key='debug').fetchone()
        print(result)
        if result:
            for f in ENS_FIELDS:
                if result[f]:
                    print("{} = {}".format(f,result[f]))


######################
# shell command line
######################

if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    test = args.test

    if not cid:
         print "please provide a college ID\n"
         parser.print_help()
         exit(-1)

    sys.exit(main())
