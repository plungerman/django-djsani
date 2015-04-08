from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.medical_history.forms import StudentForm
from djsani.medical_history.forms import AthleteForm
from djsani.core.views import get_data, put_data

#from djzbar.utils.decorators import portal_login_required

#@portal_login_required
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
    obj = get_data("cc_student_medical_manager",cid)
    if obj:
        manager = obj.fetchone()
        # check to see if they already submitted this form
        if manager and manager[table]:
            obj = get_data(table,cid)
            if obj:
                data = obj.fetchone()
                if data:
                    update = True
                    for k,v in data.items():
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
            #update_manager(table,cid)
            return HttpResponseRedirect(
                reverse_lazy("medical_history_success")
            )
        else:
            # for use at template level with dictionary filter
            for n,v in post.items():
                if n[-2:] == "_2" and v:
                    data[n[:-2]] = v
    else:
        form = eval(fname)(initial=innit, gender=request.session['gender'])
    return render_to_response(
        template,
        {
            "form":form,"stype":stype,"table":table,"cid":cid,
            "update":update,"data":data
        },
        context_instance=RequestContext(request)
    )
