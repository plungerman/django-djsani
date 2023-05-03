# -*- coding: utf-8 -*-
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
from djtools.utils.workday import get_students


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
            else:
                print("Username '{0}' does not exist".format(username))
        if user:
            #print(user)
            adult = False
            if stu.get('birth_date'):
                age = calculate_age(stu['birth_date'])
                if age >= settings.ADULT_AGE:
                    adult = True
            residency = stu.get('residency_status')[0]
            phone = stu.get('mobile')
            if not phone:
                phone = stu.get('phone')
            defaults = {
                'second_name': stu.get('middlename'),
                'residency': residency,
                'phone': phone,
                'birth_date': stu.get('birth_date'),
                'gender': stu.get('sex'),
                'address1': stu.get('addr_line1'),
                'address2': stu.get('addr_line2'),
                'city': stu.get('city'),
                'state': stu.get('st'),
                'postal_code': stu.get('zip'),
                'country': stu.get('ctry'),
                'birth_date': stu.get('birth_date'),
                'adult': adult,
                'class_year': stu.get('cl'),
            }
            profile, created = StudentProfile.objects.update_or_create(
                user=user,
                defaults=defaults,
            )


if __name__ == '__main__':
    sys.exit(main())
