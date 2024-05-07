#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import django
import os
import requests
import sys

django.setup()

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from djauth.managers import LDAPManager
from djsani.core.models import StudentProfile
from djsani.core.utils import get_manager
from djtools.utils.date import calculate_age
from djtools.utils.mail import send_mail
from djtools.utils.workday import get_students


# set up command-line options
desc = "Load student data from college directory API"

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)


def main():
    try:
        eldap = LDAPManager()
    except Exception as error:
        send_mail(
            None,
            [settings.MANAGERS[0][1],],
            '[DJ Sani] load workday students: FAIL',
            settings.MANAGERS[0][1],
            'workday_fail_email.html',
            {'error': error},
            [settings.MANAGERS[0][1]],
        )
        sys.exit(main())

    students = get_students()
    # set all profiles to status False and then
    # update to True when we have a student from API
    StudentProfile.objects.all().update(status=False)
    for stu in students:
        if stu.get('email'):
            username = stu['email'].split('@')[0]
            try:
                # fetch user
                user = User.objects.get(username=username)
                if user.first_name != stu.get('first_name'):
                    user.first_name = stu.get('first_name')
                if user.last_name != stu.get('last_name'):
                    user.last_name = stu.get('last_name')
                user.save()
            except User.DoesNotExist:
                user = None
                # or create a new user
            if not user:
                result_data = eldap.search(username, field='cn')
                if result_data:
                    groups = eldap.get_groups(result_data)
                    user = eldap.dj_create(result_data, groups=groups)
            if user:
                adult = False
                birth_date = None
                if stu.get('birth_date'):
                    birth_date = datetime.datetime.strptime(
                        stu['birth_date'],
                        '%Y-%m-%d',
                    )
                    age = calculate_age(birth_date)
                    if age >= settings.ADULT_AGE:
                        adult = True
                phone = stu.get('mobile')
                if not phone:
                    phone = stu.get('phone')
                defaults = {
                    'second_name': stu.get('second_name'),
                    'alt_name': stu.get('alt_name'),
                    'residency': stu.get('residency'),
                    'phone': phone,
                    'birth_date': birth_date,
                    'gender': stu.get('gender'),
                    'address1': stu.get('address1'),
                    'address2': stu.get('address2'),
                    'city': stu.get('city'),
                    'state': stu.get('state'),
                    'postal_code': stu.get('postal_code'),
                    'country': stu.get('country'),
                    'birth_date': stu.get('birth_date'),
                    'adult': adult,
                    'status': stu.get('status'),
                    'class_year': stu.get('class_year'),
                }
                profile, created = StudentProfile.objects.update_or_create(
                    user=user,
                    defaults=defaults,
                )
                # fetch or create the medical manager
                manager = get_manager(user, pk=False)
                if test:
                    print(manager)
            else:
                print("Username '{0}' does not exist".format(username))


if __name__ == '__main__':
    args = parser.parse_args()
    test = args.test
    if test:
        print(args)
    sys.exit(main())
