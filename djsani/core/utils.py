from django.conf import settings
from django.core.cache import cache

from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.waivers.models import Sicklecell
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import StudentMedicalContentType
from djsani.core.models import StudentMedicalManager
from djzbar.utils.informix import do_sql as do_esql

from sqlalchemy.orm.session import make_transient
from sqlalchemy import desc

EARL = settings.INFORMIX_EARL

import logging
logger = logging.getLogger(__name__)


def get_content_type(session, name):
    """
    simple function to return a content type from cache
    or get and set it if it does not exist in cache.
    default is never to expire.
    """
    ct = cache.get(name)
    if not ct:
        ct = session.query(StudentMedicalContentType).\
                filter_by(name=name).first()
        cache.set(name, ct, None)
    return ct


def _doop(session, mod, cid):
    """
    check for an object and duplicate it
    returns the new object or None
    """
    obj = session.query(mod).filter_by(college_id=cid).\
        order_by(desc(mod.id)).first()

    if obj:
        # copy the previous object to new
        session.expunge(obj)
        make_transient(obj)
        obj.id = None
        obj.created_at = None
        session.add(obj)
        # is this necessary?
        session.flush()
    return obj

def get_manager(session, cid):
    """
    returns the current student medical manager based on the date
    it was created in relation to the medical forms collection
    process start date.

    if we don't have a current manager, we create one.

    Accepts a session object and the student's college ID.
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
        # do we have a past manager?
        obj = session.query(StudentMedicalManager).filter_by(college_id=cid).\
            order_by(desc(StudentMedicalManager.id)).first()
        if obj:
            # returning student
            if obj.cc_student_immunization:
                immunization = True
            if obj.cc_athlete_sicklecell_waiver:
                # fetch the latest sicklecell waiver
                sc = session.query(Sicklecell).filter_by(college_id=cid).\
                    order_by(desc(Sicklecell.id)).first()
                if sc.proof:
                    sicklecell = True

            # check for insurance object
            ins = _doop(session, StudentHealthInsurance, cid)
            # check for student medical history
            smh = _doop(session, StudentMedicalHistory, cid)
            # check for athlete medical history
            amh = _doop(session, AthleteMedicalHistory, cid)

        # create new manager
        manager = StudentMedicalManager(
            college_id=cid, cc_student_immunization=immunization,
            cc_athlete_sicklecell_waiver=sicklecell, sitrep=False
        )
        # copy health insurance and medical histories
        session.add(manager)
        session.commit()

    return manager

def put_data(dic,table,cid=None,noquo=[]):
    """
    dic:    dictionary of data
    table:  the name of the table in the database
    cid:    create or update
    noquo:  a list of field names that do not require quotes
    """
    if cid:
        prefix = 'UPDATE %s SET ' % table
        for key,val in dic.items():
            # strip quotes
            if key not in noquo:
                try:
                    val = val.replace('"', '')
                except:
                    pass
            # informix expects 1 or 0
            if val == True:
                val = 1
            if val == False:
                val = 0
            prefix += '%s=' % key
            if noquo and key in noquo:
                prefix += '%s,' % val
            else:
                prefix += '"%s",' % val
        sql = '%s WHERE college_id=%s' % (prefix[:-1],cid)
    else:
        prefix = 'INSERT INTO %s' % table
        fields = '('
        values = 'VALUES ('
        for key,val in dic.items():
            # strip quotes
            if key not in noquo:
                try:
                    val = val.replace('"', '')
                except:
                    pass
            # informix expects 1 or 0
            if val == True:
                val = 1
            if val == False:
                val = 0
            fields +='%s,' % key
            if noquo and key in noquo:
                values +='%s,' % val
            else:
                values +='"%s",' % val
        fields = '%s)' % fields[:-1]
        values = '%s)' % values[:-1]
        sql = '%s %s %s' % (prefix,fields,values)
    do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL)
