#! /usr/bin/env python3
# -*- coding: utf-8 -*-

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
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager
from djsani.core.models import StudentProfile
from djtools.utils.date import calculate_age
from djtools.utils.workday import get_students


PHILE = os.path.join(settings.BASE_DIR, 'sql/sports_student.sql')


def get_sports(cid):
    """Private function for executing the SQL incantation."""
    with open(PHILE) as incantation:
        sql = '{0}{1}'.format(incantation.read(), cid)
    with get_connection() as connection:
        row = xsql(sql, connection).fetchall()
        return row


def main():
    minors = True
    eldap = LDAPManager()
    students = get_students()
    for stu in students:
        username = stu['username']
        try:
            # fetch user
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            # or create a new user
        if not user:
            result_data = eldap.search(username, field='cn')
            if result_data:
                groups = eldap.get_groups(result_data)
                user = eldap.dj_create(result_data, groups=groups)
        if user:
            #print(user)
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
            # sports
            sports = get_sports(stu['id'])
            for sporx in get_sports(stu['id']):
                if sporx[4]:
                    year = sporx[4].year - 1
                    sport = Sport.objects.get(code=sporx[0])
                    manager = StudentMedicalManager.objects.filter(
                        user__id=stu['id'],
                    ).filter(created_at__year=year).first()
                    if manager:
                        manager.sports.add(sport)

        else:
            print("Username '{0}' does not exist".format(username))


if __name__ == '__main__':
    sys.exit(main())
