# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from djzbar.utils.mssql import get_userid
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

def main():
    """
    main method
    """

    uid = get_userid(cid)
    print uid

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
