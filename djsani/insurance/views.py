# -*- coding: utf-8 -*-

"""Views for the insurance forms."""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_manager
from djsani.insurance.forms import AthleteForm
from djsani.insurance.forms import StudentForm
from djsani.insurance.models import StudentHealthInsurance
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group


@login_required
def index(request, stype, cid=None):
    """Main view for the insurance form."""
    medical_staff = False
    user = request.user
    staff = in_group(user, settings.STAFF_GROUP)
    student = in_group(user, settings.STUDENT_GROUP)
    if cid:
        if staff:
            medical_staff = True
        else:
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        cid = user.id

    if not student:
        if medical_staff:
            return HttpResponseRedirect(reverse_lazy('dashboard_home'))
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

    # obtain our student medical manager
    manager = get_manager(cid)
    # obtain our health insturance object
    instance = StudentHealthInsurance.objects.filter(user__id=cid).filter(
        created_at__gte=settings.START_DATE,
    ).first()

    # opt out
    oo = None
    if instance:
        oo = instance.opt_out

    # form class
    if stype == 'student':
        form_class = StudentForm
    elif stype == 'athlete':
        form_class = AthleteForm

    if request.method == 'POST':
        form = form_class(
            request.POST, request.FILES, manager=manager, instance=instance,
        )
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.user = user
            insurance.manager = manager
            insurance.save()
            # update the manager
            manager.cc_student_health_insurance = True
            manager.save()
            # opt out of insurance
            if insurance.opt_out:
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
            if staff:
                redirect = reverse_lazy('student_detail', args=[cid])
            else:
                redirect = reverse_lazy('insurance_success')
            return HttpResponseRedirect(redirect)
    else:
        # form class
        form = form_class(instance=instance, manager=manager)

    return render(
        request,
        'insurance/form.html',
        {
            'form': form,
            'oo': oo,
            'student': user,
            'medical_staff': medical_staff,
            'manager': manager,
            'group_number': settings.INSURANCE_GROUP_NUMBER,
        },
    )
