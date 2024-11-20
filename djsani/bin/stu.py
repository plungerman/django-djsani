# -*- coding: utf-8 -*-

import argparse
import django
import os
import sys

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from djsani.core.utils import get_manager
from djsani.core.models import StudentMedicalManager


# set up command-line options
desc = "Accepts as input a student's college ID"

parser = argparse.ArgumentParser(description=desc)
parser.add_argument(
    '-i',
    '--cid',
    help="Student's college ID.",
    required=True,
    dest='cid',
)


def main():
    """Grabs a student's health insurance profile."""
    print("Student's college ID = {0}".format(cid))
    student = User.objects.get(pk=cid)
    print(student)
    # managers
    managers = StudentMedicalManager.objects.filter(user__id=cid)
    manager = get_manager(cid)
    print(manager)


if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    sys.exit(main())
