from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.medical_history.waivers.forms import *
from djsani.medical_history.waivers.models import *
from djsani.core.views import get_data, get_manager, put_data, update_manager

from djzbar.utils.informix import get_session
from djtools.fields import NEXT_YEAR
from djtools.utils.convert import str_to_class

from sqlalchemy.orm import sessionmaker

import os

EARL = settings.INFORMIX_EARL

@login_required
def form(request,stype,wtype):
    cid = request.user.id
    table = "cc_%s_%s_waiver" % (stype,wtype)

    # create database session
    session = get_session(EARL)

    # check for student manager record
    manager = get_manager(session, cid)
    # form name
    fname = str_to_class(
        "djsani.medical_history.waivers.forms",
        "{}Form".format(wtype.capitalize())
    )
    # check to see if they already submitted this form
    if (manager and getattr(manager, table, None)) or not fname:
        return HttpResponseRedirect( reverse_lazy("home") )

    if request.method=='POST':
        form = fname(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # insert
            data["college_id"] = cid

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
            "form":form,"next_year":NEXT_YEAR
        },
        context_instance=RequestContext(request)
    )
