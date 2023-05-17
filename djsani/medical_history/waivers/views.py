# -*- coding: utf-8 -*-

"""Forms for medical history."""

import datetime
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djsani.core.utils import get_manager
from djsani.medical_history.waivers.models import Sicklecell
from djtools.fields import NEXT_YEAR
from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class


@login_required
def index(request, stype, wtype):
    """Generic waivers form."""
    user = request.user
    # user student type and waiver type to build table name
    table = 'cc_{0}_{1}_waiver'.format(stype, wtype)

    # check for student manager record
    manager = get_manager(user.id)
    # form name
    fname = str_to_class(
        'djsani.medical_history.waivers.forms',
        '{0}Form'.format(wtype.capitalize()),
    )
    sicklecell = None
    if wtype == 'sicklecell':
        sicklecell = Sicklecell.objects.filter(
            user=user,
        ).filter(created_at__gte=settings.START_DATE).first()

    # check to see if they already submitted this form.
    # redirect except for sicklecell waiver
    # or wtype does not return a form class (fname)
    status = getattr(manager, table, None)
    if (manager and status and wtype != 'sicklecell') or not fname:
        return HttpResponseRedirect(reverse_lazy('home'))

    if request.method == 'POST':
        form = fname(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if sicklecell:
                folder = 'sicklecell/{0}/{1}'.format(
                    user.id, manager.created_at.strftime('%Y%m%d%H%M%S%f'),
                )
                phile = handle_uploaded_file(
                    request.FILES['results_file'],
                    os.path.join(settings.UPLOADS_DIR, folder),
                )
                cd['results_file'] = '{0}/{1}'.format(folder, phile)
                cd['updated_at'] = datetime.datetime.now()
                for key, form_val in cd.items():
                    setattr(sicklecell, key, form_val)
                sicklecell.proof = True
                sicklecell.waive = False
                sicklecell.save()
            else:
                # insert
                cd['user_id'] = user.id
                cd['manager_id'] = manager.id
                model = str_to_class(
                    'djsani.medical_history.waivers.models',
                    wtype.capitalize(),
                )
                waiver = model(**cd)
                waiver.save()
            # update the manager
            setattr(manager, table, True)
            manager.save()

            return HttpResponseRedirect(reverse_lazy('waiver_success'))
    else:
        form = fname

    # check for a valid template or redirect home
    try:
        template = 'medical_history/waivers/{0}_{1}.html'.format(stype, wtype)
        os.stat(os.path.join(settings.BASE_DIR, 'templates', template))
    except Exception:
        return HttpResponseRedirect(reverse_lazy('home'))

    return render(
        request,
        template,
        {
            'form': form,
            'next_year': NEXT_YEAR,
            'student': sicklecell,
        },
    )
