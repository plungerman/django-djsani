from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djzbar.utils.decorators import portal_login_required
from djzbar.utils.mssql import get_userid

import logging
logger = logging.getLogger(__name__)

@portal_login_required
def home(request):
    return render_to_response(
        "home.html",
        {
            "sesh_earl": reverse_lazy("set_student_type")
        },
        context_instance=RequestContext(request)
    )

def login_required(request):
    cid = get_userid(request.GET.get("cid"))
    if cid:
        request.session["cid"] = cid
        return HttpResponseRedirect(
            reverse_lazy("home")
        )
    else:
        return render_to_response(
            "core/login_required.html",
            {"cid":settings.DEFAULT_CID},
            context_instance=RequestContext(request)
        )

@csrf_exempt
def set_student_type(request):
    stype = request.POST.get("student_type")
    request.session["stype"] = stype
    return HttpResponse(stype, mimetype="text/plain; charset=utf-8")

def put_data(forms,status=0,noquo=None,table=None):
    """
    status: create or update.
    noquo:  a list of field names that do not require quotes
    table:  the name of the table in the database
    """
    if status==1:
        prefix = "UPDATE %s" % table
    else:
        prefix = "INSERT INTO %s" % table
        fields = "("
        values = "VALUES ("
        for key,value in forms.items():
            fields +='%s,' % key
            values +="'%s'," % value
        fields = "%s)" % fields[:-1]
        values = "%s)" % values[:-1]
    sql = "%s %s %s" % (prefix,fields,values)
    if not settings.DEBUG:
        try:
            #do_esql(sql, key=settings.INFORMIX_DEBUG)
            do_mysql(sql)
            status = True
        except Exception, e:
            logger.debug("error = %s" % e)
            status = False
    else:
        logger.debug("sql = %s" % sql)
        status = True
    return status
