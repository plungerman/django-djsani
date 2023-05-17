# -*- coding: utf-8 -*-

"""Fetch the user's medical manager based on ID and current date."""

import argparse
import logging
import os
import sys

import django


django.setup()
# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djsani.settings.shell')

from django.conf import settings
from djsani.core.models import StudentMedicalManager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Sicklecell
from djsani.core.utils import doop
from djtools.utils.logging import seperator

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

logger = logging.getLogger('debug_logfile')


def main():
    """Obtain the users medical manager."""
    logger.debug("fetch the current user manager")
    logger.debug(seperator())
    manager = StudentMedicalManager.objects.filter(
        college_id=cid,
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
        past_man = StudentMedicalManager.objects.filter(
            college_id=cid,
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
                sc = Sicklecell.objects.filter(
                    college_id=cid,
                ).order_by('-id').first()
                if sc.proof:
                    sicklecell = True
        # create new manager
        manager = StudentMedicalManager(
            college_id=cid,
            cc_student_immunization=immunization,
            cc_athlete_sicklecell_waiver=sicklecell,
            sitrep=False,
            sitrep_athlete=False,
            concussion_baseline=concussion_baseline,
        )
        logger.debug("new manager")
        if test:
            logger.debug(manager)
        else:
            manager.save()
            logger.debug(manager)

        # check for insurance object
        doop(StudentHealthInsurance, manager)
        # check for student medical history
        doop(StudentMedicalHistory, manager)
        # check for athlete medical history
        doop(AthleteMedicalHistory, manager)


if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    test = args.test

    if test:
        logger.debug(args)

    sys.exit(main())
