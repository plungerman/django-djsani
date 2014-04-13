from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.medical_history.forms import AcademicsForm
from djsani.medical_history.forms import AthleticsForm
from djsani.medical_history.forms import _put_data, _get_data

from djtools.utils.mail import send_mail

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = [settings.INSURANCE_RECIPIENTS,]
BCC = settings.MANAGERS

def form(request,stype):
    student = {
        "cid": request.GET.get("cid"),
        "email": "%s@carthage.edu" % request.GET.get("uname")
    }
    # form name
    fname = "%sInsuranceForm" % stype.capitalize()
    # check for a record
    data = _get_insurance(student["cid"],fname)
    if request.method=='POST':
        if request.POST.get("opt_out"):
            form1 = None
            form2 = None
            data = _put_insurance([form1,form2])
        else:
            form1 = eval(fname)(request.POST,prefix="primary")
            if not request.POST.get("secondary"):
                form2 = eval(name)(request.POST,prefix="seconary")
            else:
                form2 = None
            insurance = _put_insurance(
                form1.cleaned_data,form2.cleaned_data,data["status"]
            )

        subject = "[Insurance & Emergency Information Form] %s" \
            % (student["cid"])
        send_mail(
            request,TO_LIST,subject,student["email"],
            "insurance/email.html",insurance,BCC
        )
        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        form1 = eval(fname)(data["form1"],prefix="primary")
        form2 = eval(fname)(data["form2"],prefix="secondary")
    return render_to_response(
        "insurance/form.html",
        {
            "form1": form1,"form2": form2,
        },
        context_instance=RequestContext(request)
    )


