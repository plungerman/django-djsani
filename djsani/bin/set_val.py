# -*- coding: utf-8 -*-

"""Test for the set_val() view."""

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
from djsani.core.utils import get_content_type
from djsani.core.utils import get_manager
from djsani.core.models import CHANGE
from djsani.core.models import StudentMedicalLogEntry
from djsani.core.models import StudentMedicalManager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Meni
from djsani.medical_history.waivers.models import Privacy
from djsani.medical_history.waivers.models import Reporting
from djsani.medical_history.waivers.models import Risk
from djsani.medical_history.waivers.models import Sicklecell
from djtools.utils.users import in_group


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
    '-n',
    '--name',
    required=True,
    help="Name of table field",
    dest='name',
)
parser.add_argument(
    '-p',
    '--pk',
    required=False,
    help="Primary key of this row",
    dest='pk',
)
parser.add_argument(
    '-t',
    '--table',
    required=True,
    help="Database table name",
    dest='table',
)
parser.add_argument(
    '-v',
    '--value',
    required=True,
    help="Value of table field",
    dest='post_value',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)

logger = logging.getLogger('debug_logfile')

# table names are the key, base model classes are the value
WAIVERS = {
    'cc_student_meni_waiver': Meni,
    'cc_athlete_privacy_waiver': Privacy,
    'cc_athlete_reporting_waiver': Reporting,
    'cc_athlete_risk_waiver': Risk,
    'cc_athlete_sicklecell_waiver': Sicklecell,
}
BASES = {
    'cc_student_medical_manager': StudentMedicalManager,
    'cc_student_health_insurance': StudentHealthInsurance,
    'cc_student_medical_history': StudentMedicalHistory,
    'cc_athlete_medical_history': AthleteMedicalHistory,
}
BASES.update(WAIVERS)


def main():
    """Set a single name/value pair."""
    user = User.objects.get(pk=settings.TEST_STAFF_ID)
    staff = in_group(user, settings.STAFF_GROUP)
    value = post_value
    if not cid or not name or not table or not value:
        logger.debug("Missing required parameters.")
        logger.debug("Done.")
        sys.exit()
    if not staff and int(cid) != user.id:
        logger.debug("Not staff")
        logger.debug("Done.")
        sys.exit()
    else:
        # create our dictionary to hold name/value pairs
        dic = {name: value}
        if table == 'cc_athlete_sicklecell_waiver':
            # set value = 1 if field name = 'waive' or
            # if it = 'results' since that value is
            # either Positive or Negative
            if name == 'results':
                dic['proof'] = 1
                dic['waive'] = 0
                value = 1
            elif name == 'waive':
                dic['proof'] = 0
                dic['waive'] = value
                dic['results'] = ''
            elif name == 'proof':
                dic['results'] = ''
        # retrieve student manager
        manager = get_manager(cid)
        # fetch the data
        if WAIVERS.get(table) and not pk:
            # create new waiver
            dic['college_id'] = cid
            dic['manager_id'] = manager.id
            nobj = WAIVERS[table](**dic)
            nobj.save(using='informix')
            # update the manager
            setattr(manager, table, value)
            manager.save(using='informix')
        else:
            model = BASES[table]
            nobj = model.objects.using('informix').filter(pk=pk).first()
            if nobj:
                if name == 'athlete' and str(value) == '0':
                    dic['sports'] = ''
                # green check mark for athletes
                if name == 'sitrep_athlete' and str(value) == '1':
                    if nobj.medical_consent_agreement:
                        dic['medical_consent_agreement_status'] = 1
                    if nobj.physical_evaluation_1:
                        dic['physical_evaluation_status_1'] = 1
                    if nobj.physical_evaluation_2:
                        dic['physical_evaluation_status_2'] = 1
                # update existing object
                for key, dic_val in dic.items():
                    setattr(nobj, key, dic_val)
                nobj.save(using='informix')
            else:
                logger.debug("No object found associated with ID:")
                logger.debug(pk)
                sys.exit()
            # if waiver, update manager table
            if WAIVERS.get(table):
                setattr(manager, table, value)
                manager.save(using='informix')

        # update the log entry for staff modifications
        if staff:
            message = ''
            for dkey, dval in dic.items():
                message += '{0} = {1}\n'.format(dkey, dval)
            log = StudentMedicalLogEntry(
                college_id=user.id,
                content_type_id=get_content_type(table).id,
                object_id=nobj.id,
                object_repr=nobj,
                action_flag=CHANGE,
                action_message=message,
            )
            log.save(using='informix')

    logger.debug("Done.")


if __name__ == '__main__':
    args = parser.parse_args()
    cid = args.cid
    name = args.name
    pk = args.pk
    table = args.table
    test = args.test
    post_value = args.post_value

    if test:
        logger.debug(args)

    sys.exit(main())
