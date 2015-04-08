from django.conf import settings
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, StudentMedicalManager
from djsani.core.models import StudentMedicalContentType, StudentMedicalLogEntry
from djsani.core.models import ADDITION, CHANGE
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.waivers.models import Meni, Privacy, Reporting
from djsani.medical_history.waivers.models import Risk, Sicklecell
#from djsani.medical_history.models import AthleteMedicalHistory
#from djsani.medical_history.models import StudentMedicalHistory
from djsani.core.sql import STUDENT_VITALS
from djzbar.utils.informix import do_sql as do_esql, get_engine, get_session
from djtools.utils.date import calculate_age
from djtools.utils.users import in_group
from djtools.fields import TODAY

import datetime

import logging
logger = logging.getLogger(__name__)

"""
table names are the key, base model classes are the value
"""
BASES = {
    "cc_student_health_insurance": StudentHealthInsurance,
    "cc_student_medical_manager": StudentMedicalManager,
#    "cc_student_medical_history": StudentMedicalHistory,
#    "cc_athlete_medical_history": AthleteMedicalHistory,
    "cc_student_meni_waiver": Meni,
    "cc_athlete_privacy_waiver": Privacy,
    "cc_athlete_reporting_waiver": Reporting,
    "cc_athlete_risk_waiver": Risk,
    "cc_athlete_sicklecell_waiver": Sicklecell,
}

PERSISTENT_TABLES = (
    "cc_athlete_sicklecell_waiver",
    "cc_student_health_insurance",
    "cc_student_medical_history",
    "cc_athlete_medical_history"
)

EARL = settings.INFORMIX_EARL

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


def get_manager(session, cid):
    """
    returns the current student medical manager based on the date
    it was created in relation to the medical forms collection
    process start date.

    if we don't have a current manager, we create one.

    Accepts a session object and the student's college ID.
    """

    manager = session.query(StudentMedicalManager).\
        filter_by(college_id=cid).\
        filter(StudentMedicalManager.current(settings.START_DATE)).first()

    if not manager:
        immunization = False
        sicklecell = False
        # do we have a past manager with immunization set?
        obj = session.query(StudentMedicalManager).filter_by(college_id=cid).\
            filter_by(cc_student_immunization=1).first()
        if obj:
            immunization = True
        # check if sicklecell waiver is set
            if obj.cc_athlete_sicklecell_waiver:
                sicklecell = True

        # create new manager
        manager = StudentMedicalManager(
            college_id=cid, cc_student_immunization=immunization,
            cc_athlete_sicklecell_waiver=sicklecell
        )
        session.add(manager)
        session.commit()
        # new manager means the student's profile is incomplete
        manager.status = False
    else:
        manager.status = False
        if manager.cc_student_medical_history\
        and manager.cc_student_health_insurance\
        and manager.cc_student_immunization\
        and manager.cc_student_meni_waiver:
            manager.status = True
            if manager.athlete:
                if manager.cc_athlete_medical_history\
                and manager.cc_athlete_privacy_waiver\
                and manager.cc_athlete_reporting_waiver\
                and manager.cc_athlete_risk_waiver\
                and manager.cc_athlete_sicklecell_waiver:
                    manager.status = True
                else:
                    manager.status = False

    return manager

def get_data(table, cid, fields=None):
    """
    table   = name of database table
    fields  = list of database fields to return
    """

    status = False
    sql = "SELECT "
    if fields:
        sql += ','.join(fields)
    else:
        sql += "*"
    sql += " FROM %s WHERE college_id=%s" % (table,cid)
    result = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL)
    return result

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


@csrf_exempt
@login_required
def set_type(request):
    """
    Ajax POST. Locations in use:

    Student home
        1) choose student or athlete
        2) if athlete, choose sport(s)
    Dashboard home
        1) immunization
    Dashboard student detail
        1) student or athlete
        2) if athlete, choose sport(s)
        3) insurance opt-out
        4) all waivers
    """
    staff = in_group(request.user, "MedicalStaff")

    # we need a college ID and insure no funny stuff
    cid = request.POST.get("college_id")
    if not cid:
        return HttpResponse("Error")
    if not staff and int(cid) != request.user.id:
        return HttpResponse("Not staff")

    field = request.POST.get("field")
    table = request.POST.get("table")
    switch = request.POST.get("switch")

    # create our dictionary to hold name/value pairs
    dic = {}

    # if student has sickle cell test results then
    # proof is True and waive is False
    if field[0:7] == "results":
        field = "results"
        dic["proof"] = 1
        dic["waive"] = 0
        dic["updated_at"] = datetime.datetime.now()

    # sports field is a list
    if field == "sports":
        switch = ','.join(request.POST.getlist("switch[]"))


    # if we switch from athlete then remove sports
    if field == "athlete" and switch == "0":
        dic["sports"] = ""

    # set name/value
    dic[field] = switch

    # create database session
    session = get_session(EARL)

    # retrieve student manager record
    man = get_manager(session, cid)

    # default action is a database update
    action_flag = CHANGE
    if table:
        # retrieve the object based on table name
        if table in PERSISTENT_TABLES:
            obj = session.query(BASES[table]).filter_by(college_id=cid).first()
        else:
            obj = session.query(BASES[table]).\
                filter_by(college_id=cid).\
                filter(BASES[table].current(settings.START_DATE)).first()

        if not obj:
            dic["college_id"] = cid
            # insert/create new object
            action_flag = ADDITION
            obj = BASES[table](**dic)
            session.add(obj)
            session.flush()
        else:
            # update existing object
            for key, value in dic.iteritems():
                setattr(obj, key, value)

        # update the log entry for staff modifications
        if staff:
            message = ""
            for n,v in dic.items():
                message += "{} = {}\n".format(n,v)
            logger.debug("message = {}".format(message))
            log = {
                "college_id": request.user.id,
                "content_type_id": get_content_type(session, table).id,
                "object_id": obj.id,
                "object_repr": "{}".format(obj),
                "action_flag": action_flag,
                "action_message": message
            }
            logger.debug("log = {}".format(log))
            obj = StudentMedicalLogEntry(**log)
            session.add(obj)
        # new data for the student medical manager
        if action_flag == ADDITION:
            dic = {table:1,"college_id":cid}
            obj = man
        else:
            obj = None
    else:
        obj = man

    # update the student medical manager
    if obj:
        for key, value in dic.iteritems():
            setattr(obj, key, value)

    session.commit()
    session.close()

    return HttpResponse(switch, content_type="text/plain; charset=utf-8")


@login_required
def home(request):
    staff = in_group(request.user, "MedicalStaff")
    cid = request.user.id
    my_sports = ""
    student = None
    adult = False

    engine = get_engine(EARL)
    # get student
    obj = engine.execute(
        "%s WHERE id_rec.id = '%s'" % (STUDENT_VITALS,cid)
    )
    student = obj.fetchone()
    if student:
        # save some things to Django session:
        request.session['gender'] = student.sex
        # create database session
        session = get_session()
        # retrieve student manager
        manager = get_manager(session, cid)

        # sports needs a python list
        if manager.sports:
            my_sports = manager.sports.split(",")

        # adult or minor? if we do not have a DOB, default to minor
        if staff:
            adult = True
        if student.birth_date:
            age = calculate_age(student.birth_date)
            if age >= 18:
                adult = True
        # freshman/transfer?
        first_year = False
        if student.plan_enr_sess == "RA" and student.plan_enr_yr == TODAY.year:
            first_year = True

        # show the corresponding list of sports
        if student.sex == "F":
            sports = SPORTS_WOMEN
        else:
            sports = SPORTS_MEN

        # quick switch for minor age students
        if request.GET.get("minor"):
            adult = False

        return render_to_response(
            "home.html",
            {
                "switch_earl": reverse_lazy("set_type"),
                "student":student,
                "manager":manager,
                "sports":sports,
                "my_sports":my_sports,
                "adult":adult,
                "first_year":first_year
            },
            context_instance=RequestContext(request)
        )
    #except:
    else:
        # could not find student by college_id
        # perhaps send error to home.html rather than 404
        # and set:
        # manager=sport=my_sports=first_year = None
        return Http404


def responsive_switch(request,action):
    if action=="go":
        request.session['desktop_mode']=True
    elif action=="leave":
        request.session['desktop_mode']=False
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))
