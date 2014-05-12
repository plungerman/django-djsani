from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.medical_history.waivers.forms import MeniForm
from djsani.medical_history.waivers.forms import PrivacyForm
from djsani.medical_history.waivers.forms import ReportingForm
from djsani.medical_history.waivers.forms import RiskForm
from djsani.medical_history.waivers.forms import SicklecellForm
from djsani.core.views import put_data

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NEXT_YEAR

@portal_login_required
def form(request,wtype):
    cid = request.session["cid"]
    # form name
    fname = "%sForm" % wtype.capitalize()
    if request.method=='POST':
        form = eval(fname)(request.POST)
        if form.is_valid():
            table = "athlete_%s_waiver" % wtype
            # insert
            form["cid"] = cid
            put_data(form,table)
            # update the manager
            update_manager(table,cid)
            return HttpResponseRedirect(
                reverse_lazy("waiver_success")
            )
    else:
        form = eval(fname)
    return render_to_response(
        "medical_history/waivers/%s.html" % wtype,
        {
            "form":form,"next_year":NEXT_YEAR,
        },
        context_instance=RequestContext(request)
    )
