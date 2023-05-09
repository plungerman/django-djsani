# -*- coding: utf-8 -*-

"""Views for the administrative dashboard."""

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager
from djsani.core.models import StudentProfile
from djsani.core.sql import STUDENT_VITALS
from djsani.core.sql import STUDENTS_ALPHA
from djsani.core.utils import get_manager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djtools.decorators.auth import group_required
from djtools.fields import NEXT_YEAR
from djtools.utils.convert import str_to_class
from djtools.utils.date import calculate_age
from djtools.utils.date import get_term
from djtools.utils.mail import send_mail
from djtools.utils.users import faculty_staff
from djtools.utils.users import in_group


STAFF = settings.STAFF_GROUP
COACH = settings.COACH_GROUP


def panels(request, mod, manager, content_type=None, gender=None):
    """
    Accepts a data model class, manager object, optional gender.

    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    panel = None
    mname = mod.__name__
    modo = mod.objects.filter(manager=manager).first()
    if modo:
        panel = model_to_dict(modo)
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
            'content': content_type,
            'manager': manager,
        },
        request,
    )


@login_required
def get_students(request):
    """GET or POST: returns a list of students."""
    user = request.user
    minors = False
    trees = None
    sport = None
    term = get_term()
    staff = in_group(user, STAFF)
    coach = in_group(user, COACH)
    if coach and user.is_superuser:
        coach = False
    students = StudentProfile.objects.filter(status=True)
    if request.POST:
        post = request.POST
        cyear = post.get('class')
        minors = post.get('minors')
        if staff or coach:
            sport = post.get('sport')
            # are we in print view?
            trees = post.get('print')
            if sport and staff and trees:
                # print all athletes from any given sport
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
                        sql += 'AND athlete > 0'
                    elif cyear == '4':
                        sql += 'AND cc_student_health_insurance.primary_policy_type="Gov"'
                    elif cyear == '5':
                        sql += 'AND cc_student_health_insurance.opt_out="1"'
                    elif cyear == '6':
                        sql += 'AND cc_student_health_insurance.tertiary_company="US Fire Insurance Company"'
                    else:
                        sql += 'AND cc_student_medical_manager.id IS NULL'
                elif not coach:
                    sql += 'AND prog_enr_rec.cl IN ({0})'.format(cyear)
                template = 'dashboard/students_data.inc.html'
            if sport:
                date = settings.START_DATE
                if date.month < settings.SPORTS_MONTH:
                    year = date.year
                else:
                    year = date.year + 1
                sql += """
                    AND '{0}' IN (
                    SELECT
                        TRIM(IT.invl) AS sport_code
                    FROM
                        invl_table IT
                    INNER JOIN
                        involve_rec INR
                    ON
                        TRIM(IT.invl) = TRIM(INR.invl)
                    AND
                        IT.sanc_sport = 'Y'
                    WHERE
                        TODAY BETWEEN IT.active_date AND NVL(IT.inactive_date, TODAY)
                    AND
                        YEAR(INR.end_date) = {1}
                    AND
                        INR.id = id_rec.id
                    )
                """.format(str(sport), year)
        else:
            return HttpResponse(
                "error", content_type="text/plain; charset=utf-8",
            )
    else:
        template = 'dashboard/home.html'
        if not coach:
            students.filter(class_year__in=("FN","FF","UT","PF","PN"))

    # finally
    students.order_by('user__lastname')


    ath = 0
    med = 0
    med_percent = 0
    count = len(students)
    minors_list = []

    for stu in students:
        manager = stu.get_manager()
        # some stats for display
        if manager:
            if stu.get_manager().athlete:
                ath += 1
            if stu.get_manager().cc_athlete_medical_history:
                med += 1
        # minor or adult
        adult = 'adult'
        if stu.birth_date:
            age = calculate_age(stu.birth_date)
            if age < settings.ADULT_AGE:
                adult = 'minor'
                if minors:
                    minors_list.append(stu)
        stu.adult = adult
        if trees:
            # emergency notification system
            # worday data for ENS coming soon
            # health insurance
            stu.shi = panels(request, StudentHealthInsurance, manager)
    if ath:
        med_percent = round(med/ath * 100)

    if minors_list:
        students = minors_list
    return render(
        request,
        template,
        {
            'students': students,
            'sports': Sport.objects.filter(status=True),
            'sport': sport,
            'staff': staff,
            'coach': coach,
            'med_percent': med_percent,
        },
    )


@group_required(STAFF, COACH)
def home(request):
    """Dashboard home with a list of students."""
    return get_students(request)


@group_required(STAFF)
def student_detail(request, cid=None, medium=None, content_type=None):
    """Main method for displaying student data."""
    template = 'dashboard/student_detail.html'
    if content_type:
        template = 'dashboard/student_{0}_{1}.html'.format(
            medium, content_type,
        )
    manager = None
    # search form, grab only numbers from string
    if not cid:
        cid = filter(str.isdigit, str(request.POST.get('cid')))
    # get all managers for switch select options
    managers = StudentMedicalManager.objects.filter(user__id=cid)
    # we do not want to display faculty/staff details
    # nor do we want to create a manager for them
    manid = None
    if cid and not faculty_staff(cid):
        # manager ID comes from profile switcher POST from form
        manid = request.POST.get('manid')
        # or from URL with GET variable
        if not manid:
            manid = request.GET.get('manid')
        # fetch our student
        student = User.objects.get(pk=cid)
        if student:
            if manid:
                manager = StudentMedicalManager.objects.filter(pk=manid).first()
            if not manager:
                manager = get_manager(cid)
            # calculate student's age
            try:
                age = calculate_age(student.student.birth_date)
            except Exception:
                age = None
            # emergency notification system
            ens = None
            # health insurance
            shi = panels(
                request,
                StudentHealthInsurance,
                manager,
                content_type,
            )
            # student medical history
            smh = panels(
                request,
                StudentMedicalHistory,
                manager,
                content_type,
                student.student.gender,
            )
            # athlete medical history
            amh = panels(
                request,
                AthleteMedicalHistory,
                manager,
                content_type,
                student.student.gender,
            )
            # used for staff who update info on the dashboard
            stype = 'student'
            if manager.sports and manager.sports.all():
                stype = 'athlete'
        else:
            age, ens, shi, smh, amh = (None,) * 5
            student, stype, manager = (None,) * 5
        return render(
            request,
            template,
            {
                'student': student,
                'age': age,
                'ens': ens,
                'shi': shi,
                'amh': amh,
                'smh': smh,
                'cid': cid,
                'manid': manid,
                'switch_earl': reverse_lazy('set_val'),
                'next_year': NEXT_YEAR,
                'stype': stype,
                'managers': managers,
                'manager': manager,
                'MedicalStaff': True,
            },
        )
    else:
        raise Http404


@group_required(STAFF)
def advanced_search(request):
    """Search for a student or students."""
    search = request.POST.get('search', '')
    students = None
    if len(search) > 2:
        try:
            query = int(search)
            students = StudentProfile.objects.filter(user__pk__icontains=query)
        except Exception:
            query = search
            students = StudentProfile.objects.filter(user__last_name__icontains=query)
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
            insurance = StudentHealthInsurance.objects.get(
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
