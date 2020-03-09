# -*- coding: utf-8 -*-

"""Views for the insurance forms."""

from os.path import join

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_manager
from djsani.core.utils import get_term
from djsani.insurance.forms import AthleteForm
from djsani.insurance.forms import StudentForm
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE
from djsani.insurance.models import StudentHealthInsurance
from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class
from djtools.utils.database import row2dict
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


EARL = settings.INFORMIX_ODBC


@login_required
def index(request, stype, cid=None):
    """Main view for the insurance form."""
    medical_staff = False
    user = request.user
    staff = in_group(user, settings.STAFF_GROUP)
    if cid:
        if staff:
            medical_staff = True
        else:
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        cid = user.id

    # get academic term
    term = get_term()
    # get student
    sql = """ {0}
        WHERE
        id_rec.id = "{1}"
        AND stu_serv_rec.yr = "{2}"
        AND stu_serv_rec.sess = "{3}"
    """.format(STUDENT_VITALS, cid, term['yr'], term['sess'])

    with get_connection(EARL) as connection:
        student = xsql(sql, connection).fetchone()

    if not student:
        if medical_staff:
            return HttpResponseRedirect(reverse_lazy('dashboard_home'))
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

    # obtain our student medical manager
    manager = get_manager(cid)
    # obtain our health insturance object
    insurance = StudentHealthInsurance.objects.using('informix').filter(
        college_id=cid,
    ).filter(
        created_at__gte=settings.START_DATE,
    ).first()

    update = None
    insurance_dict = row2dict(insurance)
    if insurance_dict:
        update = cid
    # opt out
    oo = insurance_dict.get('opt_out')
    # UI display for 1st, 2nd, and 3rd forms
    primary = insurance_dict.get('primary_dob')
    secondary = insurance_dict.get('secondary_dob')
    tertiary = insurance_dict.get('tertiary_dob')

    # form name
    fname = '{0}Form'.format(stype.capitalize())

    if request.method == 'POST':
        update = request.POST.get('update')
        form = str_to_class('djsani.insurance.forms', fname)(
            request.POST, request.FILES, manager=manager, insurance=insurance,
        )
        if form.is_valid():
            form = form.cleaned_data
            # update the manager
            manager.cc_student_health_insurance = True
            manager.save()
            # opt out of insurance
            oo = form.get('opt_out')
            if oo:
                # empty table
                form = STUDENT_HEALTH_INSURANCE
                if manager.athlete:
                    if not medical_staff:
                        # alert email to staff
                        if settings.DEBUG:
                            to_list = [settings.SERVER_EMAIL]
                        else:
                            to_list = settings.INSURANCE_RECIPIENTS
                        send_mail(
                            request,
                            to_list,
                            "[Health Insurance] Opt Out: {0} {1} ({2})".format(
                                user.first_name,
                                user.last_name,
                                cid,
                            ),
                            user.email,
                            'alert_email.html',
                            request,
                        )
            else:
                # deal with file uploads
                if request.FILES:
                    folder = 'insurance/{0}/{1}'.format(
                        cid, manager.created_at.strftime('%Y%m%d%H%M%S%f'),
                    )
                    sendero = join(settings.UPLOADS_DIR, folder)
                    if request.FILES.get('primary_card_front'):
                        front = handle_uploaded_file(
                            request.FILES['primary_card_front'], sendero,
                        )
                        form['primary_card_front'] = '{0}/{1}'.format(
                            folder, front,
                        )
                    else:
                        form.pop('primary_card_front', None)
                    if request.FILES.get('primary_card_back'):
                        back = handle_uploaded_file(
                            request.FILES['primary_card_back'], sendero,
                        )
                        form['primary_card_back'] = '{0}/{1}'.format(
                            folder, back,
                        )
                    else:
                        form.pop('primary_card_back', None)
                else:
                    form.pop('primary_card_front', None)
                    form.pop('primary_card_back', None)

                # student did not opt out
                form['opt_out'] = False
            # update else insert
            if update:
                # fetch our insurance object
                insu = StudentHealthInsurance.objects.using('informix').filter(
                    college_id=cid,
                ).filter(
                    created_at__gte=settings.START_DATE,
                ).first()
                # update it with form values
                for key, form_val in form.items():
                    setattr(insu, key, form_val)
            else:
                # insert
                form['college_id'] = cid
                form['manager_id'] = manager.id
                shi = StudentHealthInsurance(**form)
                shi.save(using='informix')
            if staff:
                redirect = reverse_lazy('student_detail', args=[cid])
            else:
                redirect = reverse_lazy('insurance_success')
            return HttpResponseRedirect(redirect)
        else:
            primary = insurance_dict.get('primary_dob')
            secondary = request.POST.get('secondary_dob')
            tertiary = request.POST.get('tertiary_dob')
    else:
        # form class
        form = str_to_class('djsani.insurance.forms', fname)(
            initial=insurance_dict, manager=manager, insurance=insurance,
        )

    return render(
        request,
        'insurance/form.html',
        {
            'form': form,
            'update': update,
            'oo': oo,
            'student': student,
            'medical_staff': medical_staff,
            'manager': manager,
            'primary': primary,
            'secondary': secondary,
            'tertiary': tertiary,
            'group_number': settings.INSURANCE_GROUP_NUMBER,
        },
    )
