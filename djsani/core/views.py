from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

def home(request):
    return render_to_response(
        "home.html", context_instance=RequestContext(request)
    )
