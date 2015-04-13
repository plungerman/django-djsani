from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.medical_history.forms import StudentForm, AthleteForm
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djzbar.utils.informix import get_session
from djsani.core.utils import get_manager

BASES = {
    "cc_student_medical_history": StudentMedicalHistory,
    "cc_athlete_medical_history": AthleteMedicalHistory,
    "StudentForm":StudentForm,
    "AthleteForm":AthleteForm
}

EARL = settings.INFORMIX_EARL

@login_required
def form(request,stype):
    # dictionary for initial values if "update"
    innit = {}
    # dictionary for 'yes' answer values
    data = {}
    # student id
    cid = request.user.id
    # form name
    fname = "%sForm" % stype.capitalize()
    template = "medical_history/form.html"
    # check for student record(s)
    update = False
    table = "cc_%s_medical_history" % stype

    # create database session
    session = get_session(EARL)

    # retrieve student manager record
    manager = get_manager(session, cid)

    # check to see if they already submitted this form or we
    # have data from previous years
    obj = session.query(BASES[table]).filter_by(college_id=cid).\
        filter(BASES[table].current(settings.START_DATE)).first()
    #if getattr(manager, table):
    if obj:
        update = True
        # might not need this innit bit
        for k,v in obj.items():
            innit[k] = v
        template = "medical_history/form_update.html"
    if request.method=='POST':
        post = request.POST.copy()
        form = eval(fname)(post)
        if form.is_valid():
            data = form.cleaned_data
            data["college_id"] = cid
            # update 'yes' responses with value from temp field
            for n,v in data.items():
                if v == "Yes":
                    data[n] = post["%s_2" % n]
            # remove temp fields
            for n,v in data.items():
                if n[-2:] == "_2":
                    data.pop(n)
            # insert
            put_data(data,table,noquo=["college_id"])
            # update the manager
            setattr(manager,table,True)
            session.commit()
            session.close()
            return HttpResponseRedirect(
                reverse_lazy("medical_history_success")
            )
        else:
            # for use at template level with dictionary filter
            for n,v in post.items():
                if n[-2:] == "_2" and v:
                    data[n[:-2]] = v
    else:
        form = BASES[fname](initial=obj, gender=request.session['gender'])
    return render_to_response(
        template,
        {
            "form":form,"stype":stype,"table":table,"cid":cid,
            "update":update,"data":data
        },
        context_instance=RequestContext(request)
    )
