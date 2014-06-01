from django.conf import settings
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djsani.core import *
from djsani.core.views import get_data, is_member
from djsani.medical_history.forms import StudentForm as SmedForm
from djsani.medical_history.forms import AthleteForm as AmedForm

from djzbar.utils.informix import do_sql as do_esql
from djtools.decorators.auth import group_required
from djtools.utils.date import calculate_age

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
        {"students":students,"sports":SPORTS},
        context_instance=RequestContext(request)
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST and (is_member(request.user,"Medical Staff") or request.user.is_superuser):
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

def panels(request,table,cid):
    """
    Takes database table and student ID.
    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    obj = get_data(table,cid)
    if obj:
        data = obj.fetchone()
        if data:
            innit = {}
            if table == "cc_student_medical_history":
                for k,v in data.items():
                    innit[k] = v
                form = SmedForm(initial=innit)
            if table == "cc_athlete_medical_history":
                for k,v in data.items():
                    innit[k] = v
                form = AmedForm(initial=innit)
    t = loader.get_template("dashboard/panels/%s.html" % table)
    c = RequestContext(request, {'data':data,'form':form})
    return t.render(c)

@group_required('Medical Staff')
def student_detail(request,cid=None):
    """
    main method for displaying student data
    """
    if not cid:
        # search form
        cid = request.POST.get("cid")
    if cid:
        # get student
        obj = do_esql("%s WHERE id_rec.id = '%s'" % (STUDENT_VITALS,cid))
        if obj:
            student = obj.fetchone()
            age = calculate_age(student.birth_date)
            ens = emergency_information(cid)
            shi = panels(request,"cc_student_health_insurance",cid)
            smh = panels(request,"cc_student_medical_history",cid)
            amh = panels(request,"cc_athlete_medical_history",cid)
            return render_to_response(
                "dashboard/student_detail.html",
                {
                    "student":student,"age":age,"ens":ens,
                    "shi":shi,"amh":amh,"smh":smh
                },
                context_instance=RequestContext(request)
            )
        else:
            raise Http404
    else:
        raise Http404

