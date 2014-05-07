# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from djzbar.utils.informix import do_sql
from optparse import OptionParser

"""
Fetch data from a MSSQL database
"""

# set up command-line options
desc = """
Accepts as input a college ID
"""

parser = OptionParser(description=desc)
parser.add_option(
    "-i", "--cid",
    help="Please provide a college ID.",
    dest="cid"
)

FIELDS = ['aa','beg_date','end_date','line1','line2','line3',
'phone','phone_ext','cell_carrier','opt_out']

def main():
    """
    main method
    """

    print "++MIS1++++++++++++++++++++++"
    sql = "SELECT * FROM aa_rec WHERE aa = 'MIS1' AND id='%s'" % cid
    result = do_sql(sql).fetchone()
    for f in FIELDS:
        if result[f]:
            print "%s = %s" % (f,result[f])
    print "++MIS2++++++++++++++++++++++"
    sql = "SELECT * FROM aa_rec WHERE aa = 'MIS2' AND id='%s'" % cid
    result = do_sql(sql).fetchone()
    for f in FIELDS:
        if result[f]:
            print "%s = %s" % (f,result[f])
    print "++ICE2++++++++++++++++++++++"
    sql = "SELECT * FROM aa_rec WHERE aa = 'ICE2' AND id='%s'" % cid
    result = do_sql(sql).fetchone()
    for f in FIELDS:
        if result[f]:
            print "%s = %s" % (f,result[f])
    print "++ICE+++++++++++++++++++++++"
    sql = "SELECT * FROM aa_rec WHERE aa = 'ICE' AND id='%s'" % cid
    result = do_sql(sql).fetchone()
    for f in FIELDS:
        if result[f]:
            print "%s = %s" % (f,result[f])
    print "++ENS+++++++++++++++++++++++"
    sql = "SELECT * FROM aa_rec WHERE aa = 'ENS' AND id='%s'" % cid
    result = do_sql(sql).fetchone()
    for f in FIELDS:
        if result[f]:
            print "%s = %s" % (f,result[f])

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    cid = options.cid

    mandatories = ['cid',]
    for m in mandatories:
        if not options.__dict__[m]:
            print "mandatory option is missing: %s\n" % m
            parser.print_help()
            exit(-1)

    sys.exit(main())
