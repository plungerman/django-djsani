from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djzbar.utils.decorators import portal_login_required

#@portal_login_required
def home(request):
    return render_to_response(
        "home.html",
        {
            "sesh_earl": reverse_lazy("set_student_type")
        },
        context_instance=RequestContext(request)
    )

def login_required(request):
    return render_to_response(
        "core/login_required.html",
        context_instance=RequestContext(request)
    )

@csrf_exempt
def set_student_type(request):
    stype = request.POST.get("student_type")
    request.session["stype"] = stype
    return HttpResponse(stype, mimetype="text/plain; charset=utf-8")
