from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

from djsani.core.models import StudentMedicalManager
from djsani.insurance.models import StudentHealthInsurance
from djsani.core import SPORTS, STUDENT_VITALS
from djzbar.utils.informix import do_sql as do_esql, get_engine, get_session
from djtools.utils.date import calculate_age
from djtools.utils.users import in_group
from djtools.fields import TODAY

from sqlalchemy.orm import sessionmaker

"""
table names are the key, base model classes are the value
"""
BASES = {
    "cc_student_medical_manager": StudentMedicalManager,
    "cc_student_health_insurance": StudentHealthInsurance,
}
EARL = settings.INFORMIX_EARL


def get_manager(session, cid):
    """
    returns the current student medical manager based on the date
    it was created in relation to the medical forms collection
    process start date.

    Accepts a session object and the student's college ID.
    """

    return session.query(StudentMedicalManager).\
        filter_by(college_id=cid).\
        filter(StudentMedicalManager.current(settings.START_DATE)).first()

def get_data(table,cid,fields=None):
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

def update_manager(field,cid):
    """
    simple method to update the manager table
    which we use throughout the app
    """
    put_data(
        {field:1,"college_id":cid},
        "cc_student_medical_manager",
        cid=cid,
        noquo=[field,"college_id"]
    )

@csrf_exempt
def set_type(request):
    field = request.POST.get("field")
    table = request.POST.get("table")

    if not table:
        table = StudentMedicalManager
    else:
        table = BASES[table]

    cid = request.POST.get("college_id")
    if not cid:
        cid = request.user.id

    # create database session
    session = get_session(EARL)

    # check for student manager record
    manager = get_manager(session, cid)

    # sports field is a list
    if field == "sports":
        switch = ','.join(request.POST.getlist("switch[]"))
    else:
        switch = request.POST.get("switch")

    dic = {field:switch,"college_id":cid}

    if manager:
        session.query(table).\
                filter_by(college_id=cid).\
                update(dic)
    else:
        s = table(**dic)
        session.add(s)

    session.commit()
    session.close()

    return HttpResponse(switch, content_type="text/plain; charset=utf-8")

@login_required
def home(request):
    staff = in_group(request.user, "Medical Staff")
    cid = request.user.id
    my_sports = ""
    student = None
    adult = False

    engine = get_engine(EARL)
    # get student
    obj = engine.execute(
        "%s WHERE id_rec.id = '%s'" % (STUDENT_VITALS,cid)
    )
    try:
        student = obj.fetchone()
    except:
        manager=sport=my_sports=first_year = None

    if student:
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

        # create database session
        session = get_session()

        # check for a manager
        manager = get_manager(session, cid)

        if manager:
            # sports needs a python list
            if manager.sports:
                my_sports = manager.sports.split(",")

        # quick switch for minor age students
        if request.GET.get("minor"):
            adult = False

    return render_to_response(
        "home.html",
        {
            "switch_earl": reverse_lazy("set_type"),
            "student":student,
            "manager":manager,
            "sports":SPORTS,
            "my_sports":my_sports,
            "adult":adult,
            "first_year":first_year
        },
        context_instance=RequestContext(request)
    )

def responsive_switch(request,action):
    if action=="go":
        request.session['desktop_mode']=True
    elif action=="leave":
        request.session['desktop_mode']=False
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))
