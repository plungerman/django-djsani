from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.core.views import get_manager
from djsani.insurance.models import StudentHealthInsurance
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE
from djsani.insurance.forms import StudentForm, AthleteForm

from djzbar.utils.informix import get_session
from djtools.utils.database import row2dict
from djtools.utils.users import in_group
from djtools.fields import NOW

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from textwrap import fill

@login_required
def form(request,stype,cid=None):
    if not cid:
        cid = request.user.id
    else:
        if not in_group(request.user, "Medical Staff"):
            return HttpResponseRedirect(
                reverse_lazy("home")
            )

    # create database session
    session = get_session(settings.INFORMIX_EARL)

    # get our student medical manager
    manager = get_manager(session, cid)

    # form name
    fname = "%sForm" % stype.capitalize()
    # opt out
    oo = None
    if request.method=='POST':
        # opt out of insurance
        oo = request.POST.get("opt_out")
        if oo:
            # empty table
            forms = STUDENT_HEALTH_INSURANCE
        else:
            forms = eval(fname)(request.POST)
            forms.is_valid()
            forms = forms.cleaned_data
            forms["college_id"] = cid
            forms["opt_out"] = False
        # insert or update
        if not request.POST.get("update"):
            forms["college_id"] = cid
            s = StudentHealthInsurance(**forms)
            session.add(s)
        else:
            session.query(StudentHealthInsurance).\
                filter_by(college_id=cid).\
                update(forms)

        # update the manager
        manager.cc_student_health_insurance=True
        # lastly, commit and redirect
        session.commit()
        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        obj = session.query(StudentHealthInsurance).\
            filter_by(college_id=cid).first()
        ins = {}
        update = ""
        data = row2dict(obj)
        if data:
            oo = data["opt_out"]
            update = cid
        form = eval(fname)(initial=data)
    # close database session
    session.close()
    return render_to_response(
        "insurance/form.html", {
            "form":form,"update":update,"oo":oo,
            "manager":manager,"secondary":data.get("secondary_dob")
        },
        context_instance=RequestContext(request)
    )

'''
from djsani.insurance.models import StudentHealthInsurance
from sqlalchemy import inspect
mapper = inspect(StudentHealthInsurance)
for column in mapper.attrs:
    print column.key
'''
