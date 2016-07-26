# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from django.conf import settings
from django.contrib.auth.models import User

from djzbar.utils.informix import do_sql
from djtools.utils.users import in_group

import argparse
import django

django.setup()

# set up command-line options
desc = """
    Find all users who are members of a group.
    Accepts as argument a group name (in quotes of multipe words).
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-g", "--group",
    required=True,
    help="Group name",
    dest="group"
)

def main():
    """
    main method
    """
    users = User.objects.all()
    for user in users:
        if in_group(user, group):
            print user.username, user.id

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    group = args.group

    sys.exit(main())
