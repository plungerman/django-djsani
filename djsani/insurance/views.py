# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.core.utils import get_manager
from djsani.insurance.models import StudentHealthInsurance
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE
from djsani.insurance.forms import StudentForm, AthleteForm

from djzbar.utils.informix import get_session

from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class
from djtools.utils.database import row2dict
from djtools.utils.users import in_group
from djtools.utils.mail import send_mail

from sqlalchemy.orm import sessionmaker

from os.path import join

@login_required
def form(request, stype, cid=None):
    if not cid:
        cid = request.user.id
    else:
        if not in_group(request.user, "MedicalStaff"):
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
            form = STUDENT_HEALTH_INSURANCE

            if manager.athlete:
                # alert email to staff
                if settings.DEBUG:
                    TO_LIST = [settings.SERVER_EMAIL,]
                else:
                    TO_LIST = settings.INSURANCE_RECIPIENTS
                send_mail(
                    request, TO_LIST,
                    "[Health Insurance] Opt Out: {} {} ({})".format(
                        request.user.first_name, request.user.last_name, cid
                    ), request.user.email,
                    "alert_email.html",
                    request, settings.MANAGERS
                )
        else:
            form = str_to_class(
                "djsani.insurance.forms", fname
            )(request.POST, request.FILES)
            form.is_valid()
            form = form.cleaned_data
            # deal with file uploads
            if request.FILES:
                folder = "insurance/{}/{}".format(
                    cid, manager.created_at.strftime("%Y%m%d%H%M%S%f")
                )
                p = join(settings.UPLOADS_DIR, folder)
                if request.FILES.get('primary_card_front'):
                    front = handle_uploaded_file(
                        request.FILES['primary_card_front'], p
                    )
                    form["primary_card_front"] = "{}/{}".format(folder, front)
                else:
                    form.pop("primary_card_front", None)
                if request.FILES.get('primary_card_back'):
                    back = handle_uploaded_file(
                        request.FILES['primary_card_back'], p
                    )
                    form["primary_card_back"] = "{}/{}".format(folder, back)
                else:
                    form.pop("primary_card_back", None)
            # student did not opt out
            form["opt_out"] = False
        # insert else update
        if not request.POST.get("update"):
            # insert
            form["college_id"] = cid
            form["manager_id"] = manager.id
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
        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        obj = session.query(StudentHealthInsurance).\
            filter_by(college_id=cid).\
            filter(StudentHealthInsurance.current(settings.START_DATE)).first()

        update = ""
        data = row2dict(obj)
        if data:
            oo = data["opt_out"]
            update = cid

        form = str_to_class("djsani.insurance.forms", fname)(initial=data)
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
