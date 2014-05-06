from django.conf import settings
from django.core.cache import cache
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.core import *
from djsani.medical_history.forms import StudentForm as SmedForm
from djsani.medical_history.forms import AthleteForm as AmedForm

from djzbar.utils.informix import do_sql
from djtools.decorators.auth import group_required

@group_required('Medical Staff')
def home(request):

    students = cache.get('STUDENTS_ALPHA')
    if not students:
        objs = do_sql(STUDENTS_ALPHA, key=settings.INFORMIX_DEBUG)
        students = objs.fetchall()
        cache.set('STUDENTS_ALPHA', students)

    return render_to_response(
        "dashboard/home.html",
        {"students":students,},
        context_instance=RequestContext(request)
    )

def get_data(table,cid,year=None):
    sql = "SELECT * FROM %s WHERE cid = %s" % (table,cid)
    obj = do_sql(sql)
    return obj.fetchone()

@group_required('Medical Staff')
def student_detail(request,cid):
    # get student
    obj = do_sql("%s'%s'" % (STUDENT,cid))
    student = obj.fetchone()
    # get health insurance
    insurance = get_data("student_health_insurance",cid)
    opt_out = False
    if insurance.opt_out:
        opt_out = True
    # get medical history
    medical = get_data("student_medical_history",cid)

    return render_to_response(
        "dashboard/student_detail.html",
        {"student":student,"opt_out":opt_out,},
        context_instance=RequestContext(request)
    )
