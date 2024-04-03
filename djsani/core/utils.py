# -*- coding: utf-8 -*-

"""Utilities that are used in views."""

import datetime
import os

from collections import namedtuple
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import connection
from djsani.core.models import StudentMedicalContentType
from djsani.core.models import StudentMedicalManager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory


def xsql(sql):
    """Helper function to execute SQL incantation and return the results."""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results



# doop(StudentHealthInsurance, manager)
def doop(mod, man):
    """Check for an object and duplicate it. Returns the new object or None."""
    instance = mod.objects.filter(
        user=man.user,
    ).order_by('-id').first()

    if instance:
        # copy the previous object to new
        instance.pk = None
        instance.created_at = None
        # associate the new obj with the new manager
        instance.manager_id = man.id

        # remove all tertiary values if they are athlete insurance
        if instance.__class__.__name__ == 'StudentHealthInsurance' \
          and instance.tertiary_company == settings.INSURANCE_COMPANY_NAME:
            instance.tertiary_policy_holder = ''
            instance.tertiary_dob = ''
            instance.tertiary_company = ''
            instance.tertiary_phone = ''
            instance.tertiary_policy_address = ''
            instance.tertiary_member_id = ''
            instance.tertiary_group_no = ''
            instance.tertiary_policy_type = ''
            instance.tertiary_policy_state = ''
            instance.tertiary_card = ''
        instance.save()

    return instance


def get_content_type(name):
    """Return a content type from cache or fetch and set it in cache."""
    ct = cache.get(name)
    if not ct:
        ct = StudentMedicalContentType.objects.filter(
            name=name,
        ).first()
        cache.set(name, ct, None)
    return ct


def get_manager(user, pk=True):
    """
    Returns the current student medical manager.

    it is based on the date created in relation to the medical forms
    collection process start date.

    if we don't have a current manager for a current student, we create one,
    otherwise we try to return the most recent manager.

    requires the student's college ID and START_DATE in settings file.
    """
    manager = None
    if pk:
        try:
            user = User.objects.get(pk=user)
        except Exception:
            user = None
    if user:
        # try to fetch a current manager
        # from cache or database
        manager = StudentMedicalManager.objects.filter(
            user=user,
        ).filter(created_at__gte=settings.START_DATE).first()
        # if we don't have a current manager and a current student:
        # create the new student profile by copying some things from
        # the previous manager, in addition to copying the insurance,
        # medical histories, if they exists.
        # if not current student, find the latest manager
        try:
            student = user.student
        except Exception:
            student = None
        if not manager and student and student.status:
            immunization = False
            concussion_baseline = False
            # do we have a past manager?
            past_man = StudentMedicalManager.objects.filter(
                user=user,
            ).order_by('-id').first()
            if past_man:
                # returning student
                if past_man.cc_student_immunization:
                    immunization = True
                if past_man.concussion_baseline:
                    concussion_baseline = True
            # create new manager
            manager = StudentMedicalManager(
                user=user,
                cc_student_immunization=immunization,
                sitrep=False,
                sitrep_athlete=False,
                concussion_baseline=concussion_baseline,
            )
            manager.save()
            # check for insurance object
            doop(StudentHealthInsurance, manager)
            # check for student medical history
            doop(StudentMedicalHistory, manager)
            # check for athlete medical history
            doop(AthleteMedicalHistory, manager)
        else:
            manager = StudentMedicalManager.objects.filter(user=user).order_by('-id').first()

    return manager
