from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.insurance.forms import StudentForm
from djsani.insurance.forms import AthleteForm
from djsani.core.views import get_data, put_data, update_manager

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NOW

@portal_login_required
def form(request,stype):
    cid = request.session["cid"]
    # form name
    fname = "%sForm" % stype.capitalize()
    table = "cc_student_health_insurance"
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
        # update the manager first so we can repurpose cid
        update_manager(table,cid)
        # insert or update
        if not request.POST.get("update"):
            forms["cid"] = cid
            cid = None
        noquo = ["cid","opt_out","primary_dob","secondary_dob"]
        put_data(forms,table,cid=cid,noquo=noquo)
        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        obj = get_data(table,cid)
        primary = {}
        secondary = {}
        try:
            data = obj.fetchone()
            for k,v in data.items():
                if k.startswith("primary_"):
                    primary[k[8:]] = v
                else:
                    secondary[k[10:]] = v
            update = cid
        except:
            update = ""
        form1 = eval(fname)(prefix="primary",initial=primary)
        form2 = eval(fname)(prefix="secondary",initial=secondary)
    return render_to_response(
        "insurance/form.html", {"form1":form1,"form2":form2,"update":update},
        context_instance=RequestContext(request)
    )
