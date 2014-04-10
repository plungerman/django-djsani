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
        form = InsuranceForm(request.POST)
        if form.is_valid():
            data = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if data.email:
                email = data.email
            subject = "[Insurance & Emergency Information Form] %s %s" \
                % (data.first_name,data.last_name)
            send_mail(
                request,TO_LIST,subject,email,
                "insurance/email.html",data,BCC
            )
            return HttpResponseRedirect(
                reverse_lazy("insurance_success")
            )
    else:
        form = InsuranceForm()
    return render_to_response(
        "insurance/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )
