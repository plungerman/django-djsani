from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.medical_history.forms import StudentForm
from djsani.medical_history.forms import AthleteForm
from djsani.core.views import get_data, put_data, update_manager

#from djzbar.utils.decorators import portal_login_required

#@portal_login_required
@login_required
def form(request,stype):
    cid = request.user.id
    table = "cc_%s_medical_history" % stype
    obj = get_data("cc_student_medical_manager",cid)
    if obj:
        manager = obj.fetchone()
        # check to see if they already submitted this form
        if manager[table]:
            return HttpResponseRedirect(
                reverse_lazy("home")
            )
    # form name
    fname = "%sForm" % stype.capitalize()
    if request.method=='POST':
        form = eval(fname)(request.POST)
        form.is_valid()
        data = form.cleaned_data
        data["college_id"] = cid
        # chapuza to grab dynamic textfield values
        """
        for k,v in request.POST:
            if k[-2:] == "_2":
                data[-2:]= v
        """
        # insert
        put_data(data,table,noquo=["college_id"])
        # update the manager
        update_manager(table,cid)
        return HttpResponseRedirect(
            reverse_lazy("medical_history_success")
        )
    else:
        form = eval(fname)
    return render_to_response(
        "medical_history/form.html",
        {
            "form":form,"stype":stype
        },
        context_instance=RequestContext(request)
    )
