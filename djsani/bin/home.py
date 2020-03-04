# -*- coding: utf-8 -*-

"""Test for the home view."""

import argparse
import django
import logging
import os
import sys

django.setup()
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.models import SPORTS
from djsani.core.models import SPORTS_MEN
from djsani.core.models import SPORTS_WOMEN
from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_manager
from djsani.core.utils import get_term
from djtools.utils.date import calculate_age
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group

from djmaidez.contact.data import ENS_CODES
from djmaidez.contact.data import ENS_FIELDS
from djmaidez.contact.data import MOBILE_CARRIER
from djmaidez.contact.data import RELATIONSHIP


# set up command-line options
desc = "Obtain the current data manager given the user's college ID."

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    '-c',
    '--cid',
    required=True,
    help="College ID",
    dest='cid',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)

if settings.DEBUG:
    EARL = settings.INFORMIX_ODBC_TRAIN
else:
    EARL = settings.INFORMIX_ODBC
logger = logging.getLogger('debug_logfile')


def main():
    """Home page logic for unit test."""
    # for when faculty/staff sign in here or not student found
    context_data = {}
    # fetch our user
    user = User.objects.get(pk=cid)
    # retrieve student manager (or create a new one if none exists)
    manager = get_manager(cid)
    # intialise some things
    my_sports = ''
    student = None
    adult = False
    # get academic term
    term = get_term()
    # term = {'yr': 2017, 'sess': 'RC'}
    logger.debug("get_term()")
    logger.debug(term)
    # get student
    sql = """ {0}
        WHERE
        id_rec.id = "{1}"
        AND stu_serv_rec.yr = "{2}"
        AND UPPER(stu_serv_rec.sess) = "{3}"
        AND cc_student_medical_manager.created_at > "{4}"
    """.format(
        STUDENT_VITALS, cid, term['yr'], term['sess'], settings.START_DATE,
    )
    logger.debug('STUDENT_VITALS')
    logger.debug(sql)
    with get_connection(EARL) as connection:
        student = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchone()
        if student:
            # sports needs a python list
            if manager.sports:
                my_sports = manager.sports.split(',')
                logger.debug("my_sports")
                logger.debug(my_sports)
            # adult or minor? if we do not have a DOB, default to minor
            if student.birth_date:
                age = calculate_age(student.birth_date)
                logger.debug("age")
                logger.debug(age)
                if age >= settings.ADULT_AGE:
                    adult = True
                    logger.debug('adult')
            # show the corresponding list of sports
            if student.sex == 'F':
                sports = SPORTS_WOMEN
            else:
                sports = SPORTS_MEN
            logger.debug('sports')
            logger.debug(sports)
            # context dict
            context_data = {
                'switch_earl': reverse_lazy('set_val'),
                'student': student,
                'manager': manager,
                'sports': sports,
                'my_sports': my_sports,
                'adult': adult,
                'sql': sql,
            }
            for key, cdata in context_data.items():
                logger.debug(cdata)
            # emergency contact modal form
            sql = 'SELECT * FROM aa_rec WHERE aa in {0} AND id="{1}"'.format(
                ENS_CODES, cid,
            )
            rows = xsql(sql, connection, key=settings.INFORMIX_DEBUG)
            for row in rows:
                ens = {}
                for field in ENS_FIELDS:
                    ens[field] = getattr(row, field)
                context_data[row.aa] = ens
            context_data['mobile_carrier'] = MOBILE_CARRIER
            context_data['relationship'] = RELATIONSHIP
            context_data['solo'] = True
        else:
            # returns False if not student, which returns True
            antistaff = (
                not in_group(user, 'carthageStaffStatus') and
                not in_group(user, 'carthageFacultyStatus')
            )
            logger.debug('anitstaff')
            logger.debug(antistaff)
            if antistaff:
                # could not find student by college_id
                context_data = {
                    'student': student,
                    'sports': SPORTS,
                    'solo': True,
                    'adult': adult,
                }
                # notify managers
                send_mail(
                    None,
                    settings.HOUSING_EMAIL_LIST,
                    '[Lost] Student: {0} {1} ({2})'.format(
                        user.first_name, user.last_name, cid,
                    ),
                    user.email,
                    'alert_email.html',
                    None,
                    [settings.MANAGERS[0][1]],
                )


if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    test = args.test

    if test:
        logger.debug(args)

    sys.exit(main())
