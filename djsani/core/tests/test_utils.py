# -*- coding: utf-8 -*-

"""Unit tests for the utilities code."""


import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from djsani.core.models import StudentMedicalManager
from djsani.core.utils import doop
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Sicklecell
from djtools.fields import TODAY
from djtools.utils.logging import seperator


logger = logging.getLogger('debug_logfile')
DEC = settings.DECEMBER


class CoreUtilsTestCase(TestCase):
    """Test our utilities."""

    def setUp(self):
        """Initialise our test with some data."""
        self.user = User.objects.get(pk=settings.TEST_STUDENT_ID)
        self.earl = settings.INFORMIX_ODBC_TRAIN
        self.factory = RequestFactory()

    def test_get_term(self):
        """Obtain the current academic term."""
        sd = settings.START_DATE
        term = 'RA'
        year = TODAY.year
        if (TODAY.month < sd.month) or (TODAY.month == DEC and TODAY.day > 10):
            term = 'RC'
            if TODAY.month == DEC:
                year = year + 1
        return {'yr': year, 'sess': term}

    def test_get_manager(self):
        """Obtain the users medical manager."""
        logger.debug("fetch the current user manager")
        logger.debug(seperator())
        manager = StudentMedicalManager.objects.using('informix').filter(
            college_id=self.user.id,
        ).filter(created_at__gte=settings.START_DATE).first()
        if manager:
            logger.debug("current manager")
            logger.debug(manager)
            logger.debug(manager.created_at)
        else:
            logger.debug("no current manager")
            immunization = False
            sicklecell = False
            concussion_baseline = False
            # do we have a past manager?
            past_man = StudentMedicalManager.objects.using('informix').filter(
                college_id=self.user.id,
            ).order_by('-id').first()
            if past_man:
                logger.debug("past manager")
                logger.debug(past_man)
                logger.debug(past_man.created_at)
                # returning student
                if past_man.cc_student_immunization:
                    immunization = True
                if past_man.concussion_baseline:
                    concussion_baseline = True
                # if sicklecell waiver, check the latest for proof,
                # which means always True
                if past_man.cc_athlete_sicklecell_waiver:
                    # fetch the latest sicklecell waiver
                    sc = Sicklecell.objects.using('informix').filter(
                        college_id=self.user.id,
                    ).order_by('-id').first()
                    if sc.proof:
                        sicklecell = True
            # create new manager
            manager = StudentMedicalManager(
                college_id=self.user.id,
                cc_student_immunization=immunization,
                cc_athlete_sicklecell_waiver=sicklecell,
                sitrep=False,
                sitrep_athlete=False,
                concussion_baseline=concussion_baseline,
            )
            logger.debug("new manager")
            manager.save(using='informix')
            logger.debug(manager)

            # check for insurance object
            doop(StudentHealthInsurance, manager)
            # check for student medical history
            doop(StudentMedicalHistory, manager)
            # check for athlete medical history
            doop(AthleteMedicalHistory, manager)
