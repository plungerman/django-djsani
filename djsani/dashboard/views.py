# -*- coding: utf-8 -*-

"""Views for the administrative dashboard."""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djmaidez.contact.data import ENS_CODES
from djsani.core.models import SPORTS
from djsani.core.models import SPORTS_MEN
from djsani.core.models import SPORTS_WOMEN
from djsani.core.models import StudentMedicalManager
from djsani.core.sql import STUDENT_VITALS
from djsani.core.sql import STUDENTS_ALPHA
from djsani.core.utils import get_manager
from djsani.core.utils import get_term
from djsani.emergency.models import AARec
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djtools.decorators.auth import group_required
from djtools.fields import NEXT_YEAR
from djtools.utils.convert import str_to_class
from djtools.utils.database import row2dict
from djtools.utils.date import calculate_age
from djtools.utils.mail import send_mail
from djtools.utils.users import faculty_staff
from djtools.utils.users import in_group


EARL = settings.INFORMIX_ODBC
STAFF = settings.STAFF_GROUP
COACH = settings.COACH_GROUP


def panels(request, mod, manager, content=None, gender=None):
    """
    Accepts a data model class, manager object, optional gender.

    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    panel = None
    mname = mod.__name__
    manid = manager.id
    modo = mod.objects.using('informix').filter(manager_id=manid).first()
    if modo:
        panel = row2dict(modo)
        if gender:
            form = str_to_class(
                'djsani.medical_history.forms',
                '{0}Form'.format(mname),
            )(initial=panel, gender=gender)
    template = loader.get_template('dashboard/panels/{0}.html'.format(mname))

    return template.render(
        {
            'data': panel,
            'form': form,
            'content': content,
            'manager': manager,
        },
        request,
    )


def get_students(request):
    """GET or POST: returns a list of students."""
    user = request.user
    trees = None
    sport = None
    term = get_term()
    staff = in_group(user, STAFF)
    coach = in_group(user, COACH)
    if coach and user.is_superuser:
        coach = False
    if request.POST:
        post = request.POST
        cyear = post.get('class')
        if coach:
            cyear = '3'
        if staff or coach:
            # simple protection against sql injection
            try:
                sport = int(post.get('sport'))
            except Exception:
                sport = '0'

            trees = post.get('print')
            if sport and sport != '0' and staff and trees:
                # print all athletes from any given sport
                sql = """ {0}
                    WHERE stu_serv_rec.yr = "{1}"
                    AND stu_serv_rec.sess = "{2}"
                    AND cc_student_medical_manager.created_at > "{3}"
                    AND cc_student_medical_manager.sports like "%{4}%"
                    ORDER BY lastname
                """.format(
                    STUDENT_VITALS,
                    term['yr'],
                    term['sess'],
                    settings.START_DATE,
                    str(sport),
                )
                template = 'dashboard/athletes_print.html'
            else:
                sql = """ {0}
                    AND stu_serv_rec.yr = "{1}"
                    AND stu_serv_rec.sess = "{2}"
                """.format(
                    STUDENTS_ALPHA, term['yr'], term['sess'],
                )
                if cyear in {'0', '1', '2', '3', '4', '5', '6'}:
                    if cyear == '1':
                        sql += 'AND cc_student_medical_manager.sitrep = 1'
                    elif cyear == '0':
                        sql += 'AND cc_student_medical_manager.sitrep = 0'
                    elif cyear == '3':
                        sql += 'AND cc_student_medical_manager.athlete = 1'
                    elif cyear == '4':
                        sql += 'AND cc_student_health_insurance.primary_policy_type="Gov"'
                    elif cyear == '5':
                        sql += 'AND cc_student_health_insurance.opt_out="1"'
                    elif cyear == '6':
                        sql += 'AND cc_student_medical_manager.athlete = 1'
                        sql += 'AND cc_student_health_insurance.tertiary_company="US Fire Insurance Company"'
                    else:
                        sql += 'AND cc_student_medical_manager.id IS NULL'
                else:
                    sql += 'AND prog_enr_rec.cl IN ({0})'.format(cyear)
                if sport and sport != '0':
                    sql += """
                        AND cc_student_medical_manager.sports like "%{0}%"
                    """.format(str(sport))
                sql += ' ORDER BY lastname'
                template = 'dashboard/students_data.inc.html'
        else:
            return HttpResponse(
                "error", content_type="text/plain; charset=utf-8",
            )
    else:
        template = 'dashboard/home.html'
        cl = 'AND prog_enr_rec.cl IN ("FN","FF","FR","UT","PF","PN")'
        if coach:
            cl = ''
        sql = """ {0}
            AND stu_serv_rec.yr = "{1}"
            AND stu_serv_rec.sess = "{2}"
            {3}
            ORDER BY lastname
        """.format(
            STUDENTS_ALPHA, term['yr'], term['sess'], cl,
        )
    with get_connection(EARL) as connection:
        rows = xsql(
            sql, connection, key=settings.INFORMIX_DEBUG,
        ).fetchall()

    students = None
    if rows:
        students = [dict(row) for row in rows]
        for stu in students:
            adult = 'minor'
            if stu['birth_date']:
                age = calculate_age(stu['birth_date'])
                if age >= settings.ADULT_AGE:
                    adult = 'adult'
            stu['adult'] = adult
            if trees:
                manager = get_manager(stu['id'])
                # emergency notification system
                stu['ens'] = AARec.objects.using('informix').filter(
                    id=stu['id'],
                ).filter(aa__in=ENS_CODES)
                # health insurance
                stu['shi'] = panels(request, StudentHealthInsurance, manager)

    return render(
        request, template, {
            'students': students,
            'sports': SPORTS,
            'sport': sport,
            'staff': staff,
            'coach': coach,
        },
    )


@group_required(STAFF, COACH)
def home(request):
    """Dashboard home with a list of students."""
    return get_students(request)


@login_required
def student_detail(request, cid=None, medium=None, content=None):
    """Main method for displaying student data."""
    if in_group(request.user, STAFF):
        template = 'dashboard/student_detail.html'
        if content:
            template = 'dashboard/student_{0}_{1}.html'.format(
                medium, content,
            )
        my_sports = None
        manager = None
        # search form, grab only numbers from string
        if not cid:
            cid = filter(str.isdigit, str(request.POST.get('cid')))
        # get all managers for switch select options
        managers = StudentMedicalManager.objects.using('informix').filter(
            college_id=cid,
        )
        # we do not want to display faculty/staff details
        # nor do we want to create a manager for them
        if cid and not faculty_staff(cid):
            # manager ID comes from profile switcher POST from form
            manid = request.POST.get('manid')
            # or from URL with GET variable
            if not manid:
                manid = request.GET.get('manid')
            # get student
            if manid:
                sql = """
                    {0} WHERE cc_student_medical_manager.id = {1}
                    ORDER by stu_serv_rec.stusv_no DESC
                """.format(STUDENT_VITALS, manid)
            else:
                sql = """
                    {0} WHERE id_rec.id = "{1}"
                    ORDER BY cc_student_medical_manager.created_at DESC
                """.format(STUDENT_VITALS, cid)
            with get_connection(EARL) as connection:
                student = xsql(
                    sql, connection, key=settings.INFORMIX_DEBUG,
                ).fetchone()
            if student:
                if manid:
                    manager = StudentMedicalManager.objects.using(
                        'informix',
                    ).filter(id=manid).first()
                if not manager:
                    manager = get_manager(cid)
                    # execute student vitals sql again in case we just
                    # created a new manager
                    with get_connection(EARL) as new_connection:
                        student = xsql(
                            sql, new_connection, key=settings.INFORMIX_DEBUG,
                        ).fetchone()
                # calculate student's age
                try:
                    age = calculate_age(student.birth_date)
                except Exception:
                    age = None
                # emergency notification system
                ens = AARec.objects.using('informix').filter(id=cid).filter(
                    aa__in=ENS_CODES,
                )
                # health insurance
                shi = panels(
                    request,
                    StudentHealthInsurance,
                    manager,
                    content,
                )
                # student medical history
                smh = panels(
                    request,
                    StudentMedicalHistory,
                    manager,
                    content,
                    student.sex,
                )
                # athlete medical history
                amh = panels(
                    request,
                    AthleteMedicalHistory,
                    manager,
                    content,
                    student.sex,
                )
                # used for staff who update info on the dashboard
                stype = 'student'
                if student.athlete:
                    stype = 'athlete'
                if student.sports:
                    my_sports = student.sports.split(',')
                if student.sex == 'F':
                    sports = SPORTS_WOMEN
                else:
                    sports = SPORTS_MEN
                try:
                    student_user = User.objects.get(pk=cid)
                except Exception:
                    student_user = None
            else:
                age=ens=shi=smh=amh=student=sports=stype=student_user=manager=None
            return render(
                request,
                template,
                {
                    'student': student,
                    'student_user': student_user,
                    'age': age,
                    'ens': ens,
                    'shi': shi,
                    'amh': amh,
                    'smh': smh,
                    'cid': cid,
                    'switch_earl': reverse_lazy('set_val'),
                    'sports': sports,
                    'my_sports': my_sports,
                    'next_year': NEXT_YEAR,
                    'stype': stype,
                    'managers': managers,
                    'manager': manager,
                    'MedicalStaff': True,
                },
            )
        else:
            raise Http404
    else:
        return HttpResponseRedirect(reverse_lazy('access_denied'))


@group_required(STAFF)
def advanced_search(request):
    """Search for a student or students."""
    student = request.POST.get('student', '')
    sql = None
    try:
        query = int(student)
        sql = """
            {0} WHERE id_rec.id = "{1}"
            ORDER BY cc_student_medical_manager.created_at DESC
        """.format(STUDENT_VITALS, student)
    except Exception:
        query = student.lower()
        if query and len(query) >= 3:
            sql = """
                {0} WHERE LOWER(id_rec.lastname) LIKE "%%{1}%%"
                ORDER BY lastname
            """.format(STUDENT_VITALS, query)
    if sql:
        with get_connection(EARL) as connection:
            students = xsql(
                sql, connection, key=settings.INFORMIX_DEBUG,
            ).fetchall()
    else:
        students = None

    return render(
        request,
        'dashboard/advanced_search.html',
        {'students': students},
    )


@group_required(STAFF)
def sendmail(request):
    """Send insurance data in an email to a provider."""
    message = 'error'
    insurance = None
    if request.POST:
        mid = request.POST.get('mid')
        if mid:
            insurance = StudentHealthInsurance.objects.using('informix').get(
                manager_id=mid,
            )
        email = request.POST['email']
        subject = request.POST['subject']
        cdata = {'content': request.POST['content'], 'insurance': insurance}
        send_mail(
            request,
            [email],
            subject,
            request.user.email,
            'sendmail.html',
            cdata,
        )
        message = "success"
    return HttpResponse(message, content_type='text/plain; charset=utf-8')
