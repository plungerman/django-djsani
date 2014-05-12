from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djzbar.utils.informix import do_sql as do_esql
from djzbar.utils.decorators import portal_login_required
from djtools.utils.database import do_mysql, mysql_db
from djtools.fields import NOW

def get_data(table,cid,fields=None,date=None):
    """
    table   = name of database table
    fields  = list of database fields to return
    key     = dict with unique identifier and value
    """
    status = False
    sql = "SELECT "
    if fields:
        sql += ','.join(fields)
    else:
        sql += "*"
    sql += " FROM %s WHERE cid='%s'" % (table,cid)
    if date:
        sql += " AND created_at?"
    #result = do_esql(sql)
    result = do_mysql(sql)
    return result

def put_data(dic,table,cid=None,noquo=None):
    """
    dic:    dictionary of data
    table:  the name of the table in the database
    cid:    create or update
    noquo:  a list of field names that do not require quotes
    """
    if cid:
        prefix = "UPDATE %s SET " % table
        for key,val in dic.items():
            prefix += "%s=" % key
            if noquo and key in noquo:
                prefix += "%s," % val
            else:
                prefix += "'%s'," % val
        sql = "%s WHERE cid='%s'" % (prefix[:-1],cid)
        result = do_mysql(sql,select=False)
    else:
        prefix = "INSERT INTO %s" % table
        fields = "("
        values = "VALUES ("
        for key,val in dic.items():
            fields +='%s,' % key
            if noquo and key in noquo:
                values +="%s," % val
            else:
                values +="'%s'," % val
        fields = "%s)" % fields[:-1]
        values = "%s)" % values[:-1]
        sql = "%s %s %s" % (prefix,fields,values)
        result = mysql_db(sql)
    # removed the other mysql method calls when informix tables are ready
    #result = do_esql(sql)

def update_manager(field,cid):
    """
    simple method to update the manager table
    which we use throughout the app
    """
    put_data(
        {field:True,"cid":cid},
        "student_medical_manager",
        cid=cid,
        noquo=[field]
    )

@portal_login_required
def home(request):
    return render_to_response(
        "home.html",
        {
            "sesh_earl": reverse_lazy("set_student_type")
        },
        context_instance=RequestContext(request)
    )

@csrf_exempt
def set_student_type(request):
    stype = request.POST.get("student_type")
    cid = request.POST.get("cid")
    # set the session variable for use at UI level
    request.session["stype"] = stype
    # check for existing record
    athlete = False
    table="student_medical_manager"
    if stype == "athlete":
        athlete = True
    stype = get_data(table,cid)
    update = None
    if stype:
        update = cid
    # insert or update the manager
    dic = {"athlete":athlete,"cid":cid}
    if not update:
        dic["created_at"] = NOW
    put_data(
        dic,
        "student_medical_manager",
        cid = update,
        noquo=["athlete"],
    )
    return HttpResponse(stype, mimetype="text/plain; charset=utf-8")

def responsive_switch(request,action):
    if action=="go":
        request.session['desktop_mode']=True
    elif action=="leave":
        request.session['desktop_mode']=False
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))

