from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_content_type, get_manager, get_term

from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, SPORTS
from djsani.core.models import StudentMedicalManager
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
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djtools.fields import TODAY

from datetime import datetime

"""
table names are the key, base model classes are the value
"""

WAIVERS = {
    "cc_student_meni_waiver": Meni,
    "cc_athlete_privacy_waiver": Privacy,
    "cc_athlete_reporting_waiver": Reporting,
    "cc_athlete_risk_waiver": Risk,
    "cc_athlete_sicklecell_waiver": Sicklecell,
}
BASES = {
    "cc_student_medical_manager": StudentMedicalManager,
    "cc_student_health_insurance": StudentHealthInsurance,
    "cc_student_medical_history": StudentMedicalHistory,
    "cc_athlete_medical_history": AthleteMedicalHistory,
}

BASES.update(WAIVERS)

EARL = settings.INFORMIX_EARL

@csrf_exempt
@login_required
def set_val(request):
    """
    Ajax POST for to set a single name/value pair, used mostly for
    jquery xeditable and ajax updates for student medical manager.

    Requires via POST:

    college_id
    name (database field)
    value
    pk (primary key of object to be updated)
    table
    """

    staff = in_group(request.user, "MedicalStaff")

    # we need a college ID to insure no funny stuff
    cid = request.POST.get("college_id")
    if not cid:
        return HttpResponse("Error")
    elif not staff and int(cid) != request.user.id:
        return HttpResponse("Not staff")
    else:
        # name/value pair
        name = request.POST.get("name")
        # sports field is a list
        if name == "sports":
            value = ','.join(request.POST.getlist("value[]"))
        else:
            value = request.POST.get("value")

        # table name
        table = request.POST.get("table")
        # primary key
        pk = request.POST.get("pk")
        # create our dictionary to hold name/value pairs
        dic = { name: value }
        if table == "cc_athlete_sicklecell_waiver" and name == "results":
            dic["proof"] = 1
            dic["waive"] = 0
        # create database session
        session = get_session(EARL)
        # retrieve student manager
        man = get_manager(session, cid)

        # set value = 1 if field name = "results" since that value is
        # either Positive or Negative
        if table == "cc_athlete_sicklecell_waiver" and name == "results":
            value = 1
        if WAIVERS.get(table) and not pk:
            # create new waiver
            dic["college_id"] = cid
            dic["manager_id"] = man.id
            obj = WAIVERS[table](**dic)
            session.add(obj)
            # update the manager
            setattr(man, table, value)
            session.flush()
        else:
            model = BASES[table]
            obj = session.query(model).\
                filter_by(id=pk).first()
            if not obj:
                return HttpResponse(
                    "No object found associated with ID: {}".format(pk),
                    content_type="text/plain; charset=utf-8"
                )
            else:
                if name == "athlete" and value == "0":
                    dic["sports"] = ""
                # remove the test results if a staff member is changing
                # from proof to waive or nothing
                if name == "proof" and value == "0":
                    dic["results"] = ""
                # update existing object
                for key, value in dic.iteritems():
                    setattr(obj, key, value)

            # if waiver, update manager table
            if WAIVERS.get(table):
                setattr(man, table, value)

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
                "action_flag": CHANGE,
                "action_message": message
            }
            obj = StudentMedicalLogEntry(**log)
            session.add(obj)

        session.commit()
        session.close()

        return HttpResponse(
            "success", content_type="text/plain; charset=utf-8"
        )


@login_required
def home(request):
    now = datetime.now()
    if settings.ACADEMIC_YEAR_LIMBO:
        return render_to_response(
            "closed.html",
            context_instance=RequestContext(request)
        )

    # check for medical staff
    medical_staff = in_group(request.user, "MedicalStaff")
    if medical_staff:
        request.session['medical_staff'] = True
    # check for carthage staff
    staff = in_group(request.user, "carthageStaffStatus")
    if staff:
        request.session['staff'] = True
    # fetch college id from user object
    cid = request.user.id
    # intialise some things
    my_sports = ""
    student = None
    adult = False
    if staff and not request.GET.get("adult"):
        adult = True
    # get academic term
    term = get_term()
    # get student
    sql = ''' {}
        WHERE
        id_rec.id = '{}'
        AND stu_serv_rec.yr = "{}"
        AND stu_serv_rec.sess = "{}"
    '''.format(
        STUDENT_VITALS, cid, term["yr"], term["sess"]
    )
    engine = get_engine(EARL)
    obj = engine.execute(sql)
    student = obj.fetchone()
    # create database session
    session = get_session(EARL)
    if student:
        # save some things to Django session:
        request.session['gender'] = student.sex
        # retrieve student manager
        manager = get_manager(session, cid)

        # sports needs a python list
        if manager.sports:
            my_sports = manager.sports.split(",")

        # adult or minor? if we do not have a DOB, default to minor
        if student.birth_date:
            age = calculate_age(student.birth_date)
            if age >= 18:
                adult = True

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
            "switch_earl": reverse_lazy("set_val"),
            "student":student,
            "manager":manager,
            "sports":sports,
            "my_sports":my_sports,
            "adult":adult,
        }

        # emergency contact modal form
        objs = session.query(AARec).filter_by(id=cid).\
            filter(AARec.aa.in_(ENS_CODES)).all()

        for o in objs:
            data[o.aa] = row2dict(o)
        data["mobile_carrier"] = MOBILE_CARRIER
        data["relationship"] = RELATIONSHIP
        data["solo"] = True
    else:
        # could not find student by college_id
        data = {
            "student":student,"staff":staff,"medical_staff":medical_staff,
            "sports":SPORTS,"solo":True, "adult":adult,
        }
        # notify admin
        if not staff:
            send_mail(
                request, [settings.MANAGERS[0][1],],
                "[Lost] Student: {} {} ({})".format(
                    request.user.first_name, request.user.last_name, cid
                ), request.user.email,
                "alert_email.html",
                request, settings.MANAGERS
            )

    # template depends on student or staff
    template = "home.html"
    if staff:
        template = "home_staff.html"
        # emergency contact modal form
        objs = session.query(AARec).filter_by(id=request.user.id).\
            filter(AARec.aa.in_(ENS_CODES)).all()

        for o in objs:
            data[o.aa] = row2dict(o)
        data["mobile_carrier"] = MOBILE_CARRIER
        data["relationship"] = RELATIONSHIP

    session.close()

    return render_to_response(
        template, data,
        context_instance=RequestContext(request)
    )


def responsive_switch(request,action):
    if action=="go":
        request.session['desktop_mode']=True
    elif action=="leave":
        request.session['desktop_mode']=False
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))
