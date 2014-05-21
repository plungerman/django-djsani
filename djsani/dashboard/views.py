from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from djsani.core import *
from djsani.core.views import get_data, is_member
from djsani.medical_history.forms import StudentForm as SmedForm
from djsani.medical_history.forms import AthleteForm as AmedForm

from djzbar.utils.informix import do_sql as do_esql
from djtools.decorators.auth import group_required
from djtools.utils.date import calculate_age

import logging
logger = logging.getLogger(__name__)

@group_required('Medical Staff')
def home(request):
    """
    dashboard home with a list of students
    """
    template = "dashboard/home.html",
    sql = '%s AND prog_enr_rec.cl IN ("FF","FR")' % STUDENTS_ALPHA
    objs = do_esql(sql)
    students = objs.fetchall()

    return render_to_response(
        template,
        {"students":students,"sports":SPORTS,},
        context_instance=RequestContext(request)
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST and is_member(request.user,"Medical Staff"):
        template = "dashboard/students_data.inc.html"
        sport = request.POST.get("sport")
        sql = " %s AND prog_enr_rec.cl IN (%s)" % (
            STUDENTS_ALPHA,request.POST["class"]
        )
        if sport and sport != '0':
            sql += """
                AND cc_student_medical_manager.sports like '%%%s%%'
            """ % sport
        objs = do_esql(sql)
        students = objs.fetchall()
        return render_to_response(
            template,
            {"students":students,"sports":SPORTS,},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponse("error", mimetype="text/plain; charset=utf-8")

def emergency_information(cid):
    """
    returns all of the emergency contact information for any given student
    """
    FIELDS = [
        'beg_date','end_date','line1','line2','line3',
        'phone','phone_ext','opt_out'
    ]
    CODES = ['ICE','ICE2']

    ens = ""
    for c in CODES:
        sql = "SELECT * FROM aa_rec WHERE aa = '%s' AND id='%s'" % (c,cid)
        try:
            result = do_esql(sql).fetchone()
            ens +=  "++%s++++++++++++++++++++++\n" % c
            for f in FIELDS:
                if result[f]:
                    ens += "%s = %s\n" % (f,result[f])
        except:
            pass
    return ens

@csrf_exempt
def panels(request):
    """
    ajax POST with DOM id and student ID.
    returns the data that paints the panels in the
    student detail view.
    """
    if is_member(request.user,"Medical Staff"):
        dom = request.POST.get("dom")
        cid = request.POST.get("cid")
        form = None
        data = None
        if dom == "emergency_information":
            data = emergency_information(cid)
        else:
            obj = get_data(dom,cid)
            if obj:
                data = obj.fetchone()
                innit = {}
                if dom == "cc_student_medical_history":
                    for k,v in data.items():
                        innit[k] = v
                    logger.debug("innit = %s" % innit)
                    form = SmedForm(initial=innit)
                if dom == "cc_athlete_medical_history":
                    for k,v in data.items():
                        innit[k] = v
                    form = AmedForm(initial=innit)
        return render_to_response(
            "dashboard/panels/%s.html" % dom,
            {"data":data,"form":form},
            context_instance=RequestContext(request)
        )
    else:
        raise Http404

@group_required('Medical Staff')
def student_detail(request,cid=None):
    if not cid:
        cid = request.POST.get("cid")
    if cid:
        # get student
        obj = do_esql("%s'%s'" % (STUDENT_VITALS,cid))
        student = obj.fetchone()
        age = calculate_age(student.birth_date)
        return render_to_response(
            "dashboard/student_detail.html",
            {"student":student,"age":age},
            context_instance=RequestContext(request)
        )
    else:
        raise Http404
