from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.insurance.forms import AcademicsForm
from djsani.insurance.forms import AthleticsForm
from djsani.insurance.forms import _put_data, _get_data

from djzbar.utils.decorators import portal_login_required

#@portal_login_required
def form(request,stype):
    cid = request.GET.get("cid")
    # form name
    fname = "%sForm" % stype.capitalize()
    # check for a record
    data = _get_data(cid,fname)
    if request.method=='POST':
        # has no insurance at this time
        if request.POST.get("opt_out"):
            form1 = None
            form2 = None
        else:
            form1 = eval(fname)(request.POST,prefix="primary")
            if form1.is_valid():
                form1 = form1.cleaned_data
            if not request.POST.get("secondary"):
                form2 = eval(name)(request.POST,prefix="seconary")
                if form2.is_valid():
                    form1["secondary"]=True
                    form2 = form2.cleaned_data
            else:
                form2 = None
            insurance = _put_data([form1,form2],data["status"])

        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        form1 = eval(fname)(data["form1"],prefix="primary")
        form2 = eval(fname)(data["form2"],prefix="secondary")
    return render_to_response(
        "insurance/form.html", {"form1": form1,"form2": form2,},
        context_instance=RequestContext(request)
    )

