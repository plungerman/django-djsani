# -*- coding: utf-8 -*-

"""Views for the administrative dashboard."""

import logging
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from djsani.core.forms import SportForm
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager
from djsani.core.models import StudentProfile
from djsani.core.sql import STUDENTS_ALPHA
from djsani.core.utils import get_manager
from djsani.core.utils import xsql
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


COACH = settings.COACH_GROUP
STAFF = settings.STAFF_GROUP
STUDENT = settings.STUDENT_GROUP


logger = logging.getLogger('debug_logfile')


def panels(request, mod, manager, content_type=None):
    """
    Accepts a data model class, manager object, optional content_type.

    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    panel = None
    mname = mod.__name__
    modo = mod.objects.filter(manager=manager).first()
    if modo:
        panel = model_to_dict(modo)
        panel['created_at'] = modo.created_at
        if mname in {'StudentMedicalHistory', 'AthleteMedicalHistory'}:
            form = str_to_class(
                'djsani.medical_history.forms',
                '{0}Form'.format(mname),
            )(initial=panel)
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


@group_required(STAFF, COACH)
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
    try:
        roster = user.coach
    except Exception:
        if coach and staff:
            staff = True
        else:
            coach = False
    sql = STUDENTS_ALPHA
    if request.POST:
        post = request.POST
        cyear = post.get('class')
        minors = post.get('minors')
        if staff:
            sport = post.get('sport')
            # are we in print view?
            trees = post.get('print')
            if sport and staff and trees:
                # print all athletes from any given sport
                template = 'dashboard/athlete_print.html'
            else:
                if cyear in {'0', '1', '2', '3', '4', '5', '6'}:
                    if cyear == '1':
                        sql += 'AND student_medical_manager.sitrep = 1'
                    elif cyear == '0':
                        sql += 'AND student_medical_manager.sitrep = 0'
                    elif cyear == '3':
                        sql += 'AND student_medical_manager.athlete = 1'
                    elif cyear == '4':
                        sql += 'AND student_health_insurance.primary_policy_type="Gov"'
                    elif cyear == '5':
                        sql += 'AND student_health_insurance.opt_out="1"'
                    elif cyear == '6':
                        sql += 'AND student_health_insurance.tertiary_company="US Fire Insurance Company"'
                    else:
                        sql += 'AND student_medical_manager.id IS NULL'
                else:
                    sql += 'AND student_profile.class_year IN ({0})'.format(cyear)
                template = 'dashboard/students_data.inc.html'
            if sport:
                sql += """
                    AND {0} IN (
                    SELECT
                        sport_id
                    FROM
                        student_medical_manager_sports
                    WHERE
                        studentmedicalmanager_id = student_medical_manager.id
                    )
                """.format(sport)
        else:
            return HttpResponse(
                "error", content_type="text/plain; charset=utf-8",
            )
    else:
        template = 'dashboard/home.html'
        if coach:
            sids = user.coach.get_sports(get='id')
            sql += ' AND ('
            for count, sid in enumerate(sids):
                sql += """
                {0} IN (
                SELECT
                    sport_id
                FROM
                    student_medical_manager_sports
                WHERE
                    studentmedicalmanager_id = student_medical_manager.id
                )
                """.format(sid)
                if count < len(sids) - 1:
                    sql +=' OR '
            sql += ')'
        else:
            sql += ' AND student_profile.class_year = "Freshman"'
    # lastly, order by last name
    sql += ' ORDER BY auth_user.last_name'
    students = xsql(sql)
    # some stats for display
    ath = 0
    med = 0
    med_percent = 0
    count = len(students)
    minors_list = []
    for stu in students:
        manager = get_manager(stu['id'])
        if manager:
            if manager.athlete:
                ath += 1
            if manager.cc_athlete_medical_history:
                med += 1
        # minor or adult
        adult = 'adult'
        if stu['birth_date']:
            age = calculate_age(stu['birth_date'])
            if age < settings.ADULT_AGE:
                adult = 'minor'
                if minors:
                    minors_list.append(stu)
            stu['age'] = age
            stu['adult'] = adult
        if trees:
            # emergency notification system
            # worday data for ENS coming soon
            # health insurance
            stu['shi'] = panels(request, StudentHealthInsurance, manager)
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
            'sql': sql,
        },
    )


@group_required(STAFF, COACH)
def home(request):
    """Dashboard home with a list of students."""
    return get_students(request)


@group_required(STAFF, COACH)
def sports(request, mid):
    """Manage sports for a student."""
    try:
        manager = StudentMedicalManager.objects.get(pk=mid)
    except Exception:
        form = manager = None
    if manager:
        if request.POST:
            form = SportForm(
                data=request.POST,
                instance=manager,
                use_required_attribute=settings.REQUIRED_ATTRIBUTE,
            )
            if form.is_valid():
                stu = form.save(commit=False)
                stu.user = manager.user
                stu.save()
                form.save_m2m()
                if stu.sports.exists():
                    stu.athlete = True
                else:
                    stu.athlete = False
                stu.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Sports for student {0}, {1} have been updated.".format(
                        manager.user.last_name, manager.user.first_name,
                    ),
                    extra_tags='bg-success',
                )
                coach = in_group(request.user, COACH)
                if coach:
                    redirect = reverse_lazy('dashboard_home')
                else:
                    redirect = reverse_lazy('student_detail', args=[manager.user.id])
                return HttpResponseRedirect(redirect)
        else:
            form = SportForm(instance=manager)
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Could not find a medical manager for the student.",
            extra_tags='bg-danger',
        )
        response = HttpResponseRedirect(reverse_lazy('dashboard_home'))
    return render(
        request,
        'dashboard/student_sports.html',
        {'form': form},
    )


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
    # fetch our student
    try:
        student = User.objects.get(pk=cid)
    except Exception:
        student = None

    # we do not want to display faculty/staff details
    # nor do we want to create a manager for them
    if student and in_group(student, STUDENT):




        # get all managers for switch select options
        managers = StudentMedicalManager.objects.filter(user__id=cid)
        manid = None
        # manager ID comes from profile switcher POST from form
        manid = request.POST.get('manid')
        # or from URL with GET variable
        if not manid:
            manid = request.GET.get('manid')


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
        )
        # athlete medical history
        amh = panels(
            request,
            AthleteMedicalHistory,
            manager,
            content_type,
        )
        # used for staff who update info on the dashboard
        stype = 'student'
        if manager:
            if manager.sports and manager.sports.all():
                stype = 'athlete'
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                "Could not find a medical manager for the student with ID: {0}.".format(cid),
                extra_tags='bg-success',
            )
            return HttpResponseRedirect(reverse_lazy('dashboard_home'))
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
        messages.add_message(
            request,
            messages.SUCCESS,
            "Could not find a student with ID: {0}.".format(cid),
            extra_tags='bg-success',
        )
        return HttpResponseRedirect(reverse_lazy('dashboard_home'))


@group_required(STAFF, COACH)
def search(request):
    """Search for a student or students."""
    search = request.POST.get('search', '')
    students = None
    staff = in_group(request.user, STAFF)
    if len(search) > 2:
        try:
            query = int(search)
            students = User.objects.filter(pk__icontains=query).order_by('last_name')
        except Exception:
            query = search
            students = User.objects.filter(last_name__icontains=query).order_by('last_name')
    return render(
        request,
        'dashboard/search.html',
        {'students': students, 'staff': staff},
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
        phrum = request.user.email
        send_mail(
            request,
            [email],
            subject,
            phrum,
            'sendmail.html',
            cdata,
            reply_to=[phrum,],
            bcc=[settings.MANAGERS[0][1]],
        )
        message = "success"
    return HttpResponse(message, content_type='text/plain; charset=utf-8')
