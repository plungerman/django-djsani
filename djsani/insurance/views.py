from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djsani.insurance.forms import InsuranceForm

from djtools.utils.mail import send_mail

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = [settings.INSURANCE_RECIPIENTS,]
BCC = settings.MANAGERS

def insurance_form(request):
    if request.method=='POST':
        form1 = InsuranceForm(request.POST,prefix="p")
        form2 = InsuranceForm(request.POST,prefix="s")
        if form1.is_valid() and form2.is_valid():
            student = {
                "cid": request.GET.get("cid"),
                "email": "%s@carthage.edu" % request.GET.get("uname")
            }
            data = _insert_insurance(form1,form2)
            subject = "[Insurance & Emergency Information Form] %s" \
                % (student["cid"])
            send_mail(
                request,TO_LIST,subject,student["email"],
                "insurance/email.html",data,BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("insurance_success")
            )
    else:
        form1 = InsuranceForm(prefix="p")
        form2 = InsuranceForm(prefix="s")
    return render_to_response(
        "insurance/form.html",
        {"form1": form1,"form2": form2,},
        context_instance=RequestContext(request)
    )
