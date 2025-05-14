# -*- coding: utf-8 -*-

"""Views for the insurance forms."""

from os.path import join

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djsani.core.utils import get_manager
from djtools.decorators.auth import group_required
from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class


STUDENT = settings.STUDENT_GROUP


@login_required
def index(request, stype, display=None):
    """View for student and athlete medical history."""
    # student id
    user = request.user
    # student gender
    gender = request.user.student.gender
    # model name
    mname = '{0}MedicalHistory'.format(stype.capitalize())
    # form name
    fclass = str_to_class(
        'djsani.medical_history.forms',
        '{0}Form'.format(mname),
    )
    if not fclass:
        raise Http404
    # default template
    template = 'medical_history/form_{0}.html'.format(stype)
    # check for student record(s)
    update = False
    table = 'cc_{0}_medical_history'.format(stype)
    # retrieve student manager record
    manager = get_manager(user.id)
    # retrieve our model and check to see if they already
    # submitted this form or we have data from previous years
    model = str_to_class(
        'djsani.medical_history.models', mname,
    )
    if model:
        history = model.objects.filter(user=user).filter(
            created_at__gte=settings.START_DATE,
        ).first()
    else:
        raise Http404

    # dictionary for 'yes' answer values from cleaned_data method
    cd = {}
    if history:
        cd = model_to_dict(history)
        cd['manager_id'] = manager.id
        # if current update then use the xeditable form
        # otherwise we have data from the previous year but
        # the student needs to verify it
        if getattr(manager, table):
            update = True
            if display == 'print':
                template = 'medical_history/print.html'
            else:
                template = 'medical_history/form_update.html'
    if request.method == 'POST':
        post = request.POST.copy()
        form = fclass(post, use_required_attribute=False, label_suffix='', instance=history)
        if form.is_valid():
            cd = form.cleaned_data
            # set 'yes' responses with value from temp field
            for n1, v1 in cd.items():
                # mental health check does not require explanation
                if v1 == 'Yes' and n1 != 'mental_health_check':
                    cd[n1] = post['{0}_2'.format(n1)]
            if history:
                # update
                for key, form_val in cd.items():
                    setattr(history, key, form_val)
            else:
                # remove temp fields
                for n2 in list(cd):
                    if n2[-2:] == '_2':
                        cd.pop(n2)
                cd['user'] = user
                cd['manager'] = manager
                # create new object
                history = model(**cd)
            # save out medical history object whether update or create
            history.save()
            # update the manager
            setattr(manager, table, True)
            manager.save()
            return HttpResponseRedirect(reverse_lazy('medical_history_success'))
        elif not history:
            # for use at template level with dictionary filter
            for post_name, post_value in post.items():
                if post_name[-2:] == '_2' and post_value:
                    cd[post_name[:-2]] = post_value
    else:
        form = fclass(
            initial=cd, use_required_attribute=False, label_suffix='',
        )

    return render(
        request,
        template,
        {
            'form': form,
            'gender': gender,
            'data': cd,
            'stype': stype,
            'table': table,
            'update': update,
        },
    )


@login_required
def file_upload(request, name):
    """File upload function for printed medical forms."""
    user = request.user
    # retrieve student manager record
    manager = get_manager(user.id)
    man_att = name.replace('-', '_') + '_status'
    if name == 'physical-evaluation':
        if getattr(manager, man_att + '_1') and getattr(manager, man_att + '_2'):
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        if getattr(manager, man_att):
            return HttpResponseRedirect(reverse_lazy('home'))
    # munge the field name
    slug_list = name.split('-')
    form_name = slug_list.pop(0).capitalize()
    for slug in slug_list:
        form_name += ' {0}'.format(slug.capitalize())
    form_name = ''.join(form_name.split(' '))

    fclass = str_to_class(
        'djsani.medical_history.forms',
        '{0}Form'.format(form_name),
    )
    if request.method == 'POST':
        form = fclass(request.POST, request.FILES)
        if form.is_valid():
            # folder in which we will store the file
            folder = '{0}/{1}/{2}'.format(
                name.replace('-', '_'), user.id, manager.created_at.strftime(
                    '%Y%m%d%H%M%S%f',
                ),
            )
            # complete path
            sendero = join(settings.UPLOADS_DIR, folder)
            # rename and write file to new location
            for field in form.fields:
                if request.FILES.get(field):
                    phile = handle_uploaded_file(
                        request.FILES[field], sendero,
                    )
                    setattr(manager, field, '{0}/{1}'.format(folder, phile))
                    manager.save()
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        form = fclass

    return render(
        request,
        'medical_history/{0}.html'.format(name.replace('-', '_')),
        {'form': form, 'manager': manager},
    )
