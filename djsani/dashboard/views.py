from django.conf import settings
from django.core.cache import cache
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from djsani.core import *
from djsani.core.views import get_data
from djsani.medical_history.forms import StudentForm as SmedForm
from djsani.medical_history.forms import AthleteForm as AmedForm

from djzbar.utils.informix import do_sql as do_esql
from djtools.utils.database import do_mysql
from djtools.decorators.auth import group_required

@group_required('Medical Staff')
def home(request):
    """
    dashboard home with a list of students
    """
    template = "dashboard/home.html",
    if request.POST:
        template = "dashboard/students_data.inc.html"
        sql = "%s AND prog_enr_rec.cl IN (%s)" % (
            STUDENTS_ALPHA,request.POST["class"]
        )
        objs = do_esql(sql)
        students = objs.fetchall()
        cache.set('STUDENTS_ALPHA', students)
    else:
        students = cache.get('STUDENTS_ALPHA')
        if not students:
            sql = '%s AND prog_enr_rec.cl IN ("FF","FR")' % STUDENTS_ALPHA
            objs = do_esql(sql)
            students = objs.fetchall()
            cache.set('STUDENTS_ALPHA', students)

    return render_to_response(
        template,
        {"students":students,"sports":SPORTS,},
        context_instance=RequestContext(request)
    )

def emergency_information(cid):
    """
    returns all of the emergency contact information for any given student
    """
    FIELDS = [
        'aa','beg_date','end_date','line1','line2','line3',
        'phone','phone_ext','cell_carrier','opt_out'
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

def student_health_insurance(cid):
    """
    returns the health insurance information for any given student
    """
    #insurance = get_data("student_health_insurance",cid)
    sql = "%s'%s'" % (STUDENT_HEALTH_INSURANCE,cid)
    try:
        insurance = do_mysql(sql)[0]
    except:
        insurance = None
    return insurance

def student_medical_history(cid):
    """
    returns the medical history for any given student
    """
    sql = "%s'%s'" % (STUDENT_MEDICAL_HISTORY,cid)
    try:
        medical = do_mysql(sql)[0]
    except:
        medical = None
    return medical

def athlete_medical_history(cid):
    """
    returns the medical history for any given athlete
    """
    sql = "%s'%s'" % (ATHLETE_MEDICAL_HISTORY,cid)
    try:
        medical = do_mysql(sql)[0]
    except:
        medical = None
    return medical

@csrf_exempt
@group_required('Medical Staff')
def panels(request):
    """
    ajax POST with DOM id and student ID.
    returns the data that paints the panels in the
    student detail view.
    """
    dom = request.POST.get("dom")
    cid = request.POST.get("cid")
    # don't want to eval any ole thing
    valid = [
        "emergency_information","student_health_insurance",
        "student_medical_history","athlete_medical_history"
    ]
    if dom in valid:
        # medical = get_data(dom,cid)
        # insurance = get_data(dom,cid)
        # eval = temporary solution until informix tables are built.
        # i'm looking at you, kish :-)
        m = eval(dom)
        data = m(cid)
        form = None
        if dom == "student_medical_history":
            form = SmedForm(initial=data)
        if dom == "athlete_medical_history":
            form = AmedForm(initial=data)
    return render_to_response(
        "dashboard/panels/%s.html" % dom,
        {"data":data,"form":form},
        context_instance=RequestContext(request)
    )

@group_required('Medical Staff')
def student_detail(request,cid):
    # get student
    obj = do_esql("%s'%s'" % (STUDENT_VITALS,cid))
    student = obj.fetchone()
    return render_to_response(
        "dashboard/student_detail.html",
        {"student":student,},
        context_instance=RequestContext(request)
    )
