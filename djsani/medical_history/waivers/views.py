from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.medical_history.waivers.forms import *
from djsani.medical_history.waivers.models import *
from djsani.core.views import get_data, get_manager, put_data

from djzbar.utils.informix import get_session
from djtools.fields import NEXT_YEAR
from djtools.utils.convert import str_to_class

from sqlalchemy.orm import sessionmaker

import os

import logging
logger = logging.getLogger(__name__)

@login_required
def form(request,stype,wtype):
    cid = request.user.id
    table = "cc_%s_%s_waiver" % (stype,wtype)

    # create database session
    session = get_session(settings.INFORMIX_EARL)

    # check for student manager record
    manager = get_manager(session, cid)
    # form name
    fname = str_to_class(
        "djsani.medical_history.waivers.forms",
        "{}Form".format(wtype.capitalize())
    )
    waive = True
    if wtype == "sicklecell":
        student = session.query(Sicklecell).\
        filter_by(college_id=cid).first()
        if student:
            waive = student.waive

    # check to see if they already submitted this form
    # except for those who waived sicklecell test
    if (manager and getattr(manager, table, None) and not waive) or not fname:
        return HttpResponseRedirect( reverse_lazy("home") )

    if request.method=='POST':
        form = fname(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # insert
            data["college_id"] = cid

            if student:
                for key, value in data.iteritems():
                    setattr(student, key, value)
            else:
                model = str_to_class(
                    "djsani.medical_history.waivers.models",
                    wtype.capitalize()
                )
                s = model(**data)
                session.add(s)
                # update the manager
                setattr(manager, table, True)

            session.commit()

            return HttpResponseRedirect(
                reverse_lazy("waiver_success")
            )
    else:
        form = fname

    session.close()

    # check for a valid template or redirect home
    try:
        template = "medical_history/waivers/%s_%s.html" % (stype,wtype)
        os.stat(os.path.join(settings.ROOT_DIR, "templates", template))
    except:
        return HttpResponseRedirect( reverse_lazy("home"))

    return render_to_response(
        template,
        {
            "form":form,"next_year":NEXT_YEAR,"student":student
        },
        context_instance=RequestContext(request)
    )
