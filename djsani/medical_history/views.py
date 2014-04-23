from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.medical_history.forms import AcademicsForm
from djsani.medical_history.forms import AthleticsForm
from djsani.medical_history.forms import _put_data, _get_data

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NEXT_YEAR

#@portal_login_required
def form(request,stype):
    cid = request.GET.get("cid")
    # form name
    fname = "%sForm" % stype.capitalize()
    # check for a record
    data = _get_data(cid,fname)
    if request.method=='POST':
        form = eval(fname)(request.POST)
        if form.is_valid():
            history = _put_data(
                form.cleaned_data,data["status"]
            )
            return HttpResponseRedirect(
                reverse_lazy("medical_history_success")
            )
    else:
        if data["form"]:
            form = eval(fname)(data["form"])
        else:
            form = eval(fname)
    return render_to_response(
        "medical_history/form.html",
        {
            "form":form,"data":data,"stype":stype,
        },
        context_instance=RequestContext(request)
    )
