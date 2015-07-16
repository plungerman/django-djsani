from django.conf import settings
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.forms import StudentMedicalHistoryForm
from djsani.medical_history.forms import AthleteMedicalHistoryForm
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, SPORTS
from djsani.core.models import StudentMedicalManager
from djsani.core.sql import STUDENTS_ALPHA, STUDENT_VITALS
from djsani.core.utils import get_manager
from djsani.emergency.models import AARec

from djzbar.utils.informix import do_sql as do_esql, get_session
from djtools.decorators.auth import group_required
from djtools.utils.convert import str_to_class
from djtools.utils.date import calculate_age
from djtools.utils.database import row2dict
from djtools.utils.users import in_group
from djtools.fields import NEXT_YEAR
from djmaidez.core.models import ENS_CODES

EARL = settings.INFORMIX_EARL

import logging
logger = logging.getLogger(__name__)

@group_required('MedicalStaff')
def home(request):
    """
    dashboard home with a list of students
    """
    students = None
    sql = '{} AND prog_enr_rec.cl IN ("FF","FR") '.format(STUDENTS_ALPHA)
    sql += "ORDER BY lastname"
    objs = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL)
    session = get_session(EARL)
    if objs:
        students = [dict(row) for row in objs.fetchall()]
        for s in students:
            adult = "minor"
            if s["birth_date"]:
                age = calculate_age(s["birth_date"])
                if age > 17:
                    adult = "adult"
            s["adult"] = adult
    session.close()
    return render_to_response(
        "dashboard/home.html",
        {"students":students,"sports":SPORTS},
        context_instance=RequestContext(request)
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST and (in_group(request.user,"MedicalStaff") \
      or request.user.is_superuser):
        sport = request.POST.get("sport")
        sql = " %s AND prog_enr_rec.cl IN (%s)" % (
            STUDENTS_ALPHA,request.POST["class"]
        )
        if sport and sport != '0':
            sql += """
                AND cc_student_medical_manager.sports like '%%%s%%'
            """ % sport
        #sql += GROUP_BY
        objs = do_esql(
            sql,key=settings.INFORMIX_DEBUG,earl=EARL
        )
        students = None
        if objs:
            students = objs.fetchall()
        return render_to_response(
            "dashboard/students_data.inc.html",
            {"students":students,"sports":SPORTS,},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponse("error", content_type="text/plain; charset=utf-8")

def panels(request, session, mod, manager, gender=None):
    """
    Accepts a data model class, manager object, optional gender.
    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    data = None
    mname = mod.__name__
    """
    try:
        obj = session.query(mod).filter_by(manager_id=manager.id).one()
    except:
        obj = None
    """
    manid = manager.id
    obj = session.query(mod).filter_by(manager_id=manid).first()
    if obj:
        data = row2dict(obj)
        if gender:
            form = str_to_class(
                "djsani.medical_history.forms",
                "{}Form".format(mname)
            )(initial=data, gender=gender)
    t = loader.get_template("dashboard/panels/{}.html".format(mname))
    c = RequestContext(request, {'data':data,'form':form,'manager':manager})
    return t.render(c)

@group_required('MedicalStaff')
def student_detail(request, cid=None, content=None):
    """
    main method for displaying student data
    """
    template = "dashboard/student_detail.html"
    if content:
        template = "dashboard/student_print_%s.html" % content
    my_sports = None
    if not cid:
        # search form
        cid = request.POST.get("cid")
    if cid:
        # profile switcher POST from form
        manid = request.POST.get("manid")
        session = get_session(EARL)
        # get managers
        managers = session.query(StudentMedicalManager).\
                filter_by(college_id=cid).all()
        if manid:
            manager = session.query(StudentMedicalManager).\
                filter_by(id=manid).one()
        else:
            manager = get_manager(session, cid)
        # get student
        obj = do_esql(
            "{} AND cc_student_medical_manager.id = '{}'".format(
                STUDENT_VITALS, manager.id
            ),
            key=settings.INFORMIX_DEBUG, earl=EARL
        )
        if obj:
            student = obj.fetchone()
            if student:
                try:
                    age = calculate_age(student.birth_date)
                except:
                    age = None
                ens = session.query(AARec).filter_by(id=cid).\
                    filter(AARec.aa.in_(ENS_CODES)).all()
                shi = panels(
                    request, session, StudentHealthInsurance, manager
                )
                smh = panels(
                    request, session, StudentMedicalHistory, manager, student.sex
                )
                amh = panels(
                    request, session, AthleteMedicalHistory, manager, student.sex
                )
                # used for staff who update info on the dashboard
                stype = "student"
                if student.athlete:
                    stype = "athlete"
                if student.sports:
                    my_sports = student.sports.split(",")
                if student.sex == "F":
                    sports = SPORTS_WOMEN
                else:
                    sports = SPORTS_MEN
            else:
                age=ens=shi=smh=amh=student=sports=stype=None
            return render_to_response(
                template,
                {
                    "student":student,"age":age,"ens":ens,
                    "shi":shi,"amh":amh,"smh":smh,"cid":cid,
                    "switch_earl":reverse_lazy("set_val"),
                    "sports":sports,"my_sports":my_sports,"next_year":NEXT_YEAR,
                    "stype":stype,"managers":managers,"manager":manager
                },
                context_instance=RequestContext(request)
            )
        else:
            raise Http404
    else:
        raise Http404

