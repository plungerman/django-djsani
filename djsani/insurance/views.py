from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from djsani.insurance.forms import StudentForm
from djsani.insurance.forms import AthleteForm
from djsani.core.views import get_data, put_data, update_manager

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NOW

from textwrap import fill

#@portal_login_required
@login_required
def form(request,stype):
    cid = request.user.id
    # form name
    fname = "%sForm" % stype.capitalize()
    table = "cc_student_health_insurance"
    # opt out
    oo = None
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
        forms["college_id"] = cid
        oo = request.POST.get("opt_out")
        if not oo:
            oo = 0
            # convert python dates to informix date formats
            if forms.get("primary_dob"):
                forms["primary_dob"] = "TO_DATE('%s', '%%Y-%%m-%%d')" % forms["primary_dob"]
            if forms.get("secondary_dob"):
                forms["secondary_dob"] = "TO_DATE('%s', '%%Y-%%m-%%d')" % forms["secondary_dob"]
            else:
                # OJO: wtf?
                try:
                    forms.pop("secondary_dob")
                except:
                    pass
            # strip \r\n addresses
            paddress = forms.get("primary_policy_address")
            saddress = forms.get("secondary_policy_address")
            if paddress:
                forms["primary_policy_address"] = paddress.replace('\r\n',' ')
            if saddress:
                forms["secondary_policy_address"] = saddress.replace('\r\n',' ')
        else:
            oo = 1
            forms.pop("primary_dob")
            forms.pop("secondary_dob")

        forms["opt_out"] = oo

        # insert or update
        if not request.POST.get("update"):
            forms["college_id"] = cid
            # update the manager now so we can repurpose cid
            update_manager(table,cid)
            # no cid means insert
            cid = None

        noquo = ["college_id","opt_out","primary_dob","secondary_dob"]
        put_data(forms,table,cid=cid,noquo=noquo)
        return HttpResponseRedirect(
            reverse_lazy("insurance_success")
        )
    else:
        obj = get_data("cc_student_medical_manager",cid)
        # student must have a record at this point
        manager = obj.fetchone()
        obj = get_data(table,cid)
        primary = {}
        secondary = {}
        try:
            data = obj.fetchone()
            oo = data.opt_out
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
        "insurance/form.html", {
            "form1":form1,"form2":form2,"update":update,"oo":oo,
            "manager":manager,"secondary":secondary.get("dob")
        },
        context_instance=RequestContext(request)
    )
