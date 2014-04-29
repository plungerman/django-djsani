# -*- coding: utf-8 -*-
import os, sys, datetime

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djaludir.settings")

from django.conf import settings
from django.db import connections

from djzbar.utils.informix import do_sql

from optparse import OptionParser

# set up command-line options
desc = """
Accepts as input a SQL statement from command line or from a text file.
"""

parser = OptionParser(description=desc)
parser.add_option( "-s", "--sql", help="SQL statement.", dest="sql")
parser.add_option( "-t", "--sql_text", help="Text file with sql.", dest="txt")

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def main():
    """
    main method
    """

    cursor = connections['default'].cursor()

    if sql:
        cursor.execute(sql)

    if txt:
        f = open (txt,"r")
        text = f.read()
        cursor.execute(text)
        f.close()

    for obj in dictfetchall(cursor):
    #for obj in cursor.fetchall():
        print obj

    cursor.close()

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    sql = options.sql
    txt = options.txt

    if not sql and not txt:
        print """
            provide either a sql statement or text file with sql statement.
        """
        parser.print_help()
        exit(-1)

    sys.exit(main())
