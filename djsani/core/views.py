from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_content_type, get_manager
from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, StudentMedicalManager
from djsani.core.models import StudentMedicalLogEntry
from djsani.core.models import ADDITION, CHANGE
from djsani.insurance.models import StudentHealthInsurance
from djsani.emergency.models import AARec
from djsani.medical_history.waivers.models import Meni, Privacy, Reporting
from djsani.medical_history.waivers.models import Risk, Sicklecell
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory

from djmaidez.core.models import ENS_CODES, MOBILE_CARRIER, RELATIONSHIP
from djzbar.utils.informix import get_engine, get_session
from djtools.utils.date import calculate_age
from djtools.utils.database import row2dict
from djtools.utils.users import in_group
from djtools.fields import TODAY

import datetime

"""
table names are the key, base model classes are the value
"""
BASES = {
    "cc_student_health_insurance": StudentHealthInsurance,
    "cc_student_medical_manager": StudentMedicalManager,
    "cc_student_medical_history": StudentMedicalHistory,
    "cc_athlete_medical_history": AthleteMedicalHistory,
    "cc_student_meni_waiver": Meni,
    "cc_athlete_privacy_waiver": Privacy,
    "cc_athlete_reporting_waiver": Reporting,
    "cc_athlete_risk_waiver": Risk,
    "cc_athlete_sicklecell_waiver": Sicklecell,
}

EARL = settings.INFORMIX_EARL

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
        2) meni/hep
        3) Status (sitrep)
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
    pk = request.POST.get("pk")

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

    # default action for Entry Log is a database update
    action_flag = CHANGE
    if table:
        dic["manager_id"] = man.id
        # retrieve the object based on table name
        model = BASES[table]
        if table == "cc_athlete_sicklecell_waiver" \
          and getattr(man, "cc_athlete_sicklecell_waiver"):
            obj = session.query(model).\
                filter_by(college_id=cid).filter(\
                    (Sicklecell.proof == 1) | \
                    (Sicklecell.created_at > settings.START_DATE)\
                ).first()
        else:
            obj = session.query(model).\
                filter_by(id=pk).first()
                #filter(model.current(settings.START_DATE)).first()

        if not obj:
            dic["college_id"] = cid
            # insert/create new object
            action_flag = ADDITION
            obj = model(**dic)
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
            log = {
                "college_id": request.user.id,
                "content_type_id": get_content_type(session, table).id,
                "object_id": obj.id,
                "object_repr": "{}".format(obj),
                "action_flag": action_flag,
                "action_message": message
            }
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

        # context dict
        data = {
            "switch_earl": reverse_lazy("set_type"),
            "student":student,
            "manager":manager,
            "sports":sports,
            "my_sports":my_sports,
            "adult":adult,
            "first_year":first_year
        }

        # create database session
        session = get_session(EARL)

        # emergency contact modal form
        objs = session.query(AARec).filter_by(id=cid).\
            filter(AARec.aa.in_(ENS_CODES)).all()

        for o in objs:
            data[o.aa] = row2dict(o)
        data["mobile_carrier"] = MOBILE_CARRIER
        data["relationship"] = RELATIONSHIP
        data["solo"] = True

        # chapuza to test various UI
        template = "home.html"
        if request.GET.get("template"):
            template = "home_{}.html".format(request.GET.get("template"))

        return render_to_response(
            template, data,
            context_instance=RequestContext(request)
        )
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
