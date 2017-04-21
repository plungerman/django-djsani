from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.medical_history.waivers.forms import *
from djsani.medical_history.waivers.models import *
from djsani.core.utils import get_manager

from djzbar.utils.informix import get_session
from djtools.fields import NEXT_YEAR
from djtools.utils.convert import str_to_class
from djtools.fields.helpers import handle_uploaded_file

import os

from os.path import join


@login_required
def form(request, stype, wtype):
    cid = request.user.id
    table = "cc_{}_{}_waiver".format(stype, wtype)

    # create database session
    session = get_session(settings.INFORMIX_EARL)

    # check for student manager record
    manager = get_manager(session, cid)
    # form name
    fname = str_to_class(
        "djsani.medical_history.waivers.forms",
        "{}Form".format(wtype.capitalize())
    )
    sicklecell = None
    if wtype == "sicklecell":
        sicklecell = session.query(Sicklecell).\
            filter_by(college_id=cid).filter(\
                (Sicklecell.proof == 1) | \
                (Sicklecell.created_at > settings.START_DATE)\
            ).first()

    # check to see if they already submitted this form.
    # redirect except for sicklecell waiver
    # or wtype does not return a form class (fname)
    if (manager and getattr(manager, table, None) and not sicklecell) or not fname:
        return HttpResponseRedirect( reverse_lazy("home") )

    if request.method=='POST':
        form = fname(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # deal with file uploads
            if request.FILES.get('results_file'):
                folder = "sicklecell/{}/{}".format(
                    cid, manager.created_at.strftime("%Y%m%d%H%M%S%f")
                )
                p = join(settings.UPLOADS_DIR, folder)
                phile = handle_uploaded_file(
                    request.FILES['results_file'], p
                )
                data['results_file'] = '{}/{}'.format(folder, phile)

            if sicklecell:
                # update student's sicklecell waiver record
                data["updated_at"] = datetime.datetime.now()
                for key, value in data.iteritems():
                    setattr(sicklecell, key, value)
            else:
                # insert
                data["college_id"] = cid
                data["manager_id"] = manager.id
                model = str_to_class(
                    "djsani.medical_history.waivers.models",
                    wtype.capitalize()
                )
                s = model(**data)
                session.add(s)
                # update the manager
                setattr(manager, table, True)

            session.commit()
            session.close()

            return HttpResponseRedirect(
                reverse_lazy("waiver_success")
            )
    else:
        form = fname

    session.close()

    # check for a valid template or redirect home
    try:
        template = "medical_history/waivers/{}_{}.html".format(stype, wtype)
        os.stat(os.path.join(settings.ROOT_DIR, "templates", template))
    except:
        return HttpResponseRedirect( reverse_lazy("home") )

    return render_to_response(
        template,
        {
            "form":form,"next_year":NEXT_YEAR,"student":sicklecell
        },
        context_instance=RequestContext(request)
    )
