# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_manager, get_term
from djsani.insurance.models import StudentHealthInsurance
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE
from djsani.insurance.forms import StudentForm, AthleteForm

from djzbar.utils.informix import get_session, get_engine

from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class
from djtools.utils.database import row2dict
from djtools.utils.users import in_group
from djtools.utils.mail import send_mail

from os.path import join

EARL = settings.INFORMIX_EARL

@login_required
def form(request, stype, cid=None):
    medical_staff=False
    staff = in_group(request.user, "MedicalStaff")
    if not cid:
        cid = request.user.id
    else:
        if not staff:
            return HttpResponseRedirect(
                reverse_lazy('home')
            )
        else:
            medical_staff=True

    # get academic term
    term = get_term()
    # get student
    '''
        AND stu_serv_rec.yr = '{}'
        AND stu_serv_rec.sess = '{}'
    '''
    sql = ''' {}
        WHERE
        id_rec.id = '{}'
    '''.format(
        STUDENT_VITALS, cid, term['yr'], term['sess']
    )

    engine = get_engine(EARL)
    obj = engine.execute(sql)
    student = obj.fetchone()

    if not student:
        if medical_staff:
            return HttpResponseRedirect(
                reverse_lazy('dashboard_home')
            )
        else:
            return HttpResponseRedirect(
                reverse_lazy('home')
            )

    # create database session
    session = get_session(settings.INFORMIX_EARL)
    # obtain our student medical manager
    manager = get_manager(session, cid)
    # obtain our health insturance object
    insurance = session.query(StudentHealthInsurance).\
        filter_by(college_id=cid).\
        filter(StudentHealthInsurance.current(settings.START_DATE)).first()

    update = None
    data = row2dict(insurance)
    if data:
        update = cid
    # opt out
    oo = data.get('opt_out')
    # UI display for 1st, 2nd, and 3rd forms
    primary = data.get('primary_dob')
    secondary = data.get('secondary_dob')
    tertiary = data.get('tertiary_dob')

    # form name
    fname = '{}Form'.format(stype.capitalize())
    # form class
    form = str_to_class('djsani.insurance.forms', fname)(
        initial=data, manager=manager, insurance=insurance
    )

    if request.method=='POST':
        update = request.POST.get('update')
        form = str_to_class(
            'djsani.insurance.forms', fname
        )(request.POST, request.FILES, manager=manager, insurance=insurance)
        if form.is_valid():
            form = form.cleaned_data
            # opt out of insurance
            oo = form.get('opt_out')
            if oo:
                if manager.athlete and not staff:
                    # alert email to staff
                    if settings.DEBUG:
                        TO_LIST = [settings.SERVER_EMAIL,]
                    else:
                        TO_LIST = settings.INSURANCE_RECIPIENTS
                    send_mail(
                        request, TO_LIST,
                        u"[Health Insurance] Opt Out: {} {} ({})".format(
                            request.user.first_name,request.user.last_name,cid
                        ), request.user.email,
                        'alert_email.html',
                        request, settings.MANAGERS
                    )
                else:
                    # empty table
                    form = STUDENT_HEALTH_INSURANCE
            else:
                # deal with file uploads
                if request.FILES:
                    folder = 'insurance/{}/{}'.format(
                        cid, manager.created_at.strftime('%Y%m%d%H%M%S%f')
                    )
                    p = join(settings.UPLOADS_DIR, folder)
                    if request.FILES.get('primary_card_front'):
                        front = handle_uploaded_file(
                            request.FILES['primary_card_front'], p
                        )
                        form['primary_card_front'] = '{}/{}'.format(
                            folder, front
                        )
                    else:
                        form.pop('primary_card_front', None)
                    if request.FILES.get('primary_card_back'):
                        back = handle_uploaded_file(
                            request.FILES['primary_card_back'], p
                        )
                        form['primary_card_back'] = '{}/{}'.format(
                            folder, back
                        )
                    else:
                        form.pop('primary_card_back', None)
                else:
                    form.pop('primary_card_front', None)
                    form.pop('primary_card_back', None)

                # student did not opt out
                form['opt_out'] = False
            # insert else update
            if not update:
                # insert
                form['college_id'] = cid
                form['manager_id'] = manager.id
                s = StudentHealthInsurance(**form)
                session.add(s)
            else:
                # fetch our insurance object
                obj = session.query(StudentHealthInsurance).\
                    filter_by(college_id=cid).\
                    filter(StudentHealthInsurance.current(settings.START_DATE)).\
                    first()
                # update it with form values
                for key, value in form.iteritems():
                    setattr(obj, key, value)

            # update the manager
            manager.cc_student_health_insurance=True
            # lastly, commit and redirect
            session.commit()
            if staff:
                redirect = reverse_lazy('student_detail', args=[cid])
            else:
                redirect = reverse_lazy('insurance_success')
            return HttpResponseRedirect(redirect)
        else:
            primary = data.get('primary_dob')
            secondary = request.POST.get('secondary_dob')
            tertiary = request.POST.get('tertiary_dob')

    # close database session
    session.close()

    return render(
        request, 'insurance/form.html', {
            'form':form,'update':update,'oo':oo,'student':student,
            'medical_staff':medical_staff, 'manager':manager,
            'primary':primary,'secondary':secondary,'tertiary':tertiary
        }
    )

'''
from djsani.insurance.models import StudentHealthInsurance
from sqlalchemy import inspect
mapper = inspect(StudentHealthInsurance)
for column in mapper.attrs:
    print column.key
'''
