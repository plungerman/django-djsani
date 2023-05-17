# -*- coding: utf-8 -*-

import django
import os
import sys

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

django.setup()

from django.conf import settings
from djsani.insurance.models import StudentHealthInsurance
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE
from optparse import OptionParser

# set up command-line options
desc = """
Accepts as input a student's college ID and
optional True/False for opting out of insurance
"""

parser = OptionParser(description=desc)
parser.add_option(
    '-i',
    '--ID',
    help="Student's college ID.",
    dest='cid',
)
parser.add_option(
    '-o',
    '--OPT_OUT',
    help="True or false.",
    dest='opt_out',
)


def main():
    """Grabs a student's health insurance profile."""
    print("Student's college ID = {0}".format(cid))
    shi = StudentHealthInsurance.objects.filter_by(college_id=cid).first()
    print(shi.__dict__)
    # empty the table for opt_out
    if opt_out:
        shi.update(STUDENT_HEALTH_INSURANCE)
        shi.save()
        print(shi.__dict__)


if __name__ == '__main__':
    (options, args) = parser.parse_args()
    cid = options.cid
    opt_out = options.opt_out

    mandatories = ['cid',]
    for m in mandatories:
        if not options.__dict__[m]:
            print("mandatory option is missing: %s\n" % m)
            parser.print_help()
            exit(-1)

    sys.exit(main())
