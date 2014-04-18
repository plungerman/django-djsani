from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.medical_history.waivers.forms import PrivacyForm
from djsani.medical_history.waivers.forms import ReportingForm
from djsani.medical_history.waivers.forms import RiskForm
from djsani.medical_history.waivers.forms import SickleForm
from djsani.medical_history.waivers.forms import _put_data, _get_data

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NEXT_YEAR

@portal_login_required
def form(request,wtype):
    cid = request.GET.get("cid")
    # form name
    fname = "%sForm" % wtype.capitalize()
    # check for a record
    data = _get_data(cid,fname)
    if request.method=='POST':
        form = eval(fname)(request.POST)
        if form.is_valid():
            waiver = _put_data(
                form.cleaned_data,data["status"]
            )
            return HttpResponseRedirect(
                reverse_lazy("waiver_success")
            )
    else:
        if data["form"]:
            form = eval(fname)(data["form"])
        else:
            form = eval(fname)
    return render_to_response(
        "medical_history/waivers/%s.html" % wtype,
        {
            "form":form,"data":data,"next_year":NEXT_YEAR,
        },
        context_instance=RequestContext(request)
    )
