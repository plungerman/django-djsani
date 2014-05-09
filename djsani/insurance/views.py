from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.insurance.forms import StudentForm
from djsani.insurance.forms import AthleteForm
from djsani.core.views import put_data, update_manager

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NOW

@portal_login_required
def form(request,stype):
    cid = request.session["cid"]
    # form name
    fname = "%sForm" % stype.capitalize()
    if request.method=='POST':
        # primary
        form1 = eval(fname)(request.POST,prefix="primary")
        form1.is_valid()
        form1 = form1.cleaned_data
        # secondary
        form2 = eval(fname)(request.POST,prefix="secondary")
        form2.is_valid()
        form2 = form2.cleaned_data
        forms = {}
        for k,v in form1.items():
            if v == "None":
                v = ""
            forms["primary_%s" % k] = v
        for k,v in form2.items():
            if v == "None":
                v = ""
            forms["secondary_%s" % k] = v
        forms["cid"] = cid
        oo = request.POST.get("opt_out")
        if not oo:
            oo = 0
        else:
            oo = 1
        forms["opt_out"] = oo
        forms["created_at"] = NOW
        table = "student_health_insurance"
        # insert
        forms["cid"] = cid
        put_data(forms,table)
        # update the manager
        update_manager(table,cid)
        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        form1 = eval(fname)(prefix="primary")
        form2 = eval(fname)(prefix="secondary")
    return render_to_response(
        "insurance/form.html", {"form1": form1,"form2": form2,},
        context_instance=RequestContext(request)
    )
