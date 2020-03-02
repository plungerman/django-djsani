# -*- coding: utf-8 -*-

"""Utilities that are used in views."""

from django.conf import settings
from django.core.cache import cache
from djsani.core.models import StudentMedicalContentType
from djsani.core.models import StudentMedicalManager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Sicklecell
from djtools.fields import TODAY


def get_content_type(session, name):
    """Return a content type from cache or fetch and set it in cache."""
    ct = cache.get(name)
    if not ct:
        ct = session.query(StudentMedicalContentType).\
                filter_by(name=name).first()
        cache.set(name, ct, None)
    return ct


def _doop(session, mod, man):
    """Check for an object and duplicate it. Returns the new object or None."""
    # django duplicate object
    # obj = Foo.objects.get(pk=<some_existing_pk>)
    # obj.pk = None
    # obj.save()

    obj = session.query(mod).filter_by(college_id=man.college_id).\
        order_by(desc(mod.id)).first()

    if obj:
        # copy the previous object to new
        session.expunge(obj)
        make_transient(obj)
        obj.id = None
        obj.created_at = None
        # associate the new obj with the new manager
        obj.manager_id = man.id
        session.add(obj)
        # in case we need PK id
        session.flush()
    return obj


def get_term():
    """Obtain the current academic term."""
    sd = settings.START_DATE
    term = 'RA'
    year = TODAY.year
    if ((TODAY.month < sd.month) or (TODAY.month == 12 and TODAY.day > 10)):
        term = 'RC'
        if TODAY.month == 12:
            year = year + 1
    return {'yr': year, 'sess': term}


def get_manager(session, cid):
    """
    Returns the current student medical manager.

    it is based on the date created in relation to the medical forms
    collection process start date.

    if we don't have a current manager, we create one.

    accepts a session object and the student's college ID.
    Requires START_DATE in settings file
    """
    # try to fetch a current manager
    # from cache or database
    manager = session.query(StudentMedicalManager).\
        filter_by(college_id=cid).\
        filter(StudentMedicalManager.current(settings.START_DATE)).first()
    # if we don't have a current manager:
    #    (could be a first time returning student or new FR or transfer)
    # create the new student profile by copying some things from
    # the previous manager, in addition to copying the insurance,
    # medical histories, sicklecell waiver if they exists.
    if not manager:
        immunization = False
        sicklecell = False
        concussion_baseline = False
        # do we have a past manager?
        obj = session.query(StudentMedicalManager).filter_by(college_id=cid).\
            order_by(desc(StudentMedicalManager.id)).first()
        if obj:
            # returning student
            if obj.cc_student_immunization:
                immunization = True
            if obj.concussion_baseline:
                concussion_baseline = True
            # if sicklecell waiver, check the latest for proof,
            # which means always True
            if obj.cc_athlete_sicklecell_waiver:
                # fetch the latest sicklecell waiver
                sc = session.query(Sicklecell).filter_by(college_id=cid).\
                    order_by(desc(Sicklecell.id)).first()
                if sc.proof:
                    sicklecell = True

        # create new manager
        manager = StudentMedicalManager(
            college_id=cid, cc_student_immunization=immunization,
            cc_athlete_sicklecell_waiver=sicklecell, sitrep=False,
            sitrep_athlete=False, concussion_baseline=concussion_baseline
        )
        # add manager
        session.add(manager)
        session.flush()

        # check for insurance object
        ins = _doop(session, StudentHealthInsurance, manager)
        # check for student medical history
        smh = _doop(session, StudentMedicalHistory, manager)
        # check for athlete medical history
        amh = _doop(session, AthleteMedicalHistory, manager)

        session.commit()

    return manager
