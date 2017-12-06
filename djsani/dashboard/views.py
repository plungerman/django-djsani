from django.conf import settings
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.forms import StudentMedicalHistoryForm
from djsani.medical_history.forms import AthleteMedicalHistoryForm
from djsani.insurance.models import StudentHealthInsurance
from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, SPORTS
from djsani.core.models import StudentMedicalManager
from djsani.core.sql import STUDENTS_ALPHA, STUDENT_VITALS
from djsani.core.utils import get_manager, get_term
from djsani.emergency.models import AARec

from djzbar.utils.informix import do_sql as do_esql, get_session
from djtools.decorators.auth import group_required
from djtools.utils.convert import str_to_class
from djtools.utils.date import calculate_age
from djtools.utils.database import row2dict
from djtools.utils.users import in_group, faculty_staff
from djtools.utils.mail import send_mail
from djtools.fields import NEXT_YEAR
from djmaidez.core.models import ENS_CODES

EARL = settings.INFORMIX_EARL

@group_required('MedicalStaff')
def home(request):
    """
    dashboard home with a list of students
    """
    students = None
    # get academic term
    term = get_term()
    sql = ''' {}
        AND stu_serv_rec.yr = "{}"
        AND stu_serv_rec.sess = "{}"
        AND prog_enr_rec.cl IN ("FN","FF","FR","UT","PFF")
        ORDER BY lastname
    '''.format(
        STUDENTS_ALPHA, term["yr"], term["sess"]
    )

    objs = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL)
    if objs:
        students = [dict(row) for row in objs.fetchall()]
        for s in students:
            adult = "minor"
            if s["birth_date"]:
                age = calculate_age(s["birth_date"])
                if age > 17:
                    adult = "adult"
            s["adult"] = adult
    return render(
        request, "dashboard/home.html",
        {"students":students,"sports":SPORTS}
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST and (in_group(request.user,"MedicalStaff") \
      or request.user.is_superuser):
        sport = request.POST.get("sport")
        # get academic term
        term = get_term()
        sql = ''' {}
            AND stu_serv_rec.yr = "{}"
            AND stu_serv_rec.sess = "{}"
        '''.format(
            STUDENTS_ALPHA, term["yr"], term["sess"]
        )
        c = request.POST["class"]
        if c in ['0','1','2','3','4']:
            if c == '1':
                sql += "AND cc_student_medical_manager.sitrep = 1"
            elif c == '0':
                sql += "AND cc_student_medical_manager.sitrep = 0"
            elif c == '3':
                sql += "AND cc_student_medical_manager.athlete = 1"
            elif c == '4':
                sql += "AND cc_student_health_insurance.primary_policy_type='Gov'"
            else:
                sql += "AND cc_student_medical_manager.id IS NULL"
        else:
            sql += "AND prog_enr_rec.cl IN ({})".format(c)
        if sport and sport != '0':
            sql += """
                AND cc_student_medical_manager.sports like '%%%s%%'
            """ % sport
        sql += " ORDER BY lastname"

        objs = do_esql(
            sql,key=settings.INFORMIX_DEBUG,earl=EARL
        )
        students = None
        if objs:
            students = [dict(row) for row in objs.fetchall()]
            for s in students:
                adult = "minor"
                if s["birth_date"]:
                    age = calculate_age(s["birth_date"])
                    if age > 17:
                        adult = "adult"
                s["adult"] = adult
        return render(
            request, "dashboard/students_data.inc.html",
            {"students":students,"sports":SPORTS,}
        )
    else:
        return HttpResponse("error", content_type="text/plain; charset=utf-8")

def panels(request, session, mod, manager,content,gender=None):
    """
    Accepts a data model class, manager object, optional gender.
    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    data = None
    mname = mod.__name__
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

    return t.render(
        {'data':data,'form':form,'content':content,'manager':manager}, request
    )

@group_required('MedicalStaff')
def student_detail(request, cid=None, medium=None, content=None):
    """
    main method for displaying student data
    """
    term = get_term()
    template = "dashboard/student_detail.html"
    if content:
        template = "dashboard/student_{}_{}.html".format(
            medium, content
        )
    my_sports = None
    manager = None
    session = get_session(EARL)
    # search form, grab only numbers from string
    if not cid:
        cid = filter(str.isdigit, str(request.POST.get("cid")))
    # get all managers for switch select options
    managers = session.query(StudentMedicalManager).\
        filter_by(college_id=cid).all()
    # we do not want to display faculty/staff details
    # nor do we want to create a manager for them
    if cid and not faculty_staff(cid):
        # manager ID comes from profile switcher POST from form
        manid = request.POST.get("manid")
        # or from URL with GET variable
        if not manid:
            manid = request.GET.get("manid")
        # get student
        if manid:
            sql = '''
                {} WHERE cc_student_medical_manager.id = {}
                ORDER by stu_serv_rec.stusv_no DESC
        '''.format(STUDENT_VITALS, manid)
        else:
            sql = '''
                {} WHERE id_rec.id = "{}"
                END
                ORDER BY cc_student_medical_manager.created_at DESC
            '''.format(STUDENT_VITALS, cid)
        obj = do_esql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)
        if obj:
            student = obj.fetchone()
            if student:
                if manid:
                    manager = session.query(StudentMedicalManager).\
                        filter_by(id=manid).one()
                if not manager:
                    manager = get_manager(session, cid)
                    # execute student vitals sql again in case we just created
                    # a new manager
                    obj = do_esql(sql, key=settings.INFORMIX_DEBUG, earl=EARL)
                    student = obj.fetchone()
                # calculate student's age
                try:
                    age = calculate_age(student.birth_date)
                except:
                    age = None
                # emergency notification system
                ens = session.query(AARec).filter_by(id=cid).\
                    filter(AARec.aa.in_(ENS_CODES)).all()
                # health insurance
                shi = panels(
                    request, session, StudentHealthInsurance, manager, content
                )
                # student medical history
                smh = panels(
                    request,session,StudentMedicalHistory,manager,content,
                    student.sex
                )
                # athlete medical history
                amh = panels(
                    request,session,AthleteMedicalHistory,manager,content,
                    student.sex
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
                try:
                    student_user = User.objects.get(pk=cid)
                except:
                    student_user = None
            else:
                age=ens=shi=smh=amh=student=sports=stype=student_user=manager=None
            return render(
                request, template,
                {
                    "student":student,"student_user":student_user,"age":age,
                    "ens":ens, "shi":shi,"amh":amh,"smh":smh,"cid":cid,
                    "switch_earl":reverse_lazy("set_val"),
                    "sports":sports,"my_sports":my_sports,
                    "next_year":NEXT_YEAR,"stype":stype,"managers":managers,
                    "manager":manager,"MedicalStaff":True
                }
            )
        else:
            raise Http404
    else:
        raise Http404


@group_required('MedicalStaff')
def advanced_search(request):
    q = request.POST.get("lastname", "").lower()
    if q and len(q) >= 3:
        sql = '''
            {} WHERE LOWER(id_rec.lastname) LIKE "%%{}%%"
            ORDER BY lastname
        '''.format(STUDENT_VITALS, q)
        students = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=EARL).fetchall()
    else:
        students = None
    return render(
        request, "dashboard/advanced_search.html",
        {"students":students,}
    )


@group_required('MedicalStaff')
def sendmail(request):
    message = "error"
    if request.POST:
        email = request.POST['email']
        subject = request.POST['subject']
        data = {'content': request.POST['content']}
        send_mail(
            request, [email], subject, request.user.email,
            "sendmail.html", data, settings.MANAGERS
        )
        message = "success"
    return HttpResponse(message, content_type="text/plain; charset=utf-8")

