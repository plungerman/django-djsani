from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext, loader

from djsani.emergency.models import AARec

from djzbar.utils.informix import get_session
from djmaidez.core.models import ENS_CODES, MOBILE_CARRIER, RELATIONSHIP

EARL = settings.INFORMIX_EARL

@login_required
def emergency_contact(request):
    """
    Emergency contact modal generator
    """
    cid = request.GET.get('UserID', '')

    session = get_session(EARL)

    sql = 'SELECT * FROM aa_rec WHERE aa in {} AND id="{}"'.format(
        ENS_CODES,cid
    )
    objs = session.execute(sql)

    data = {}

    for o in objs:
        row = {}
        for field in ENS_FIELDS:
            try:
                value = getattr(o, field).decode('cp1252').encode('utf-8')
            except:
                value = getattr(o, field)
            row[field] = value
        data[o.aa] = row

    data['mobile_carrier'] = MOBILE_CARRIER
    data['relationship'] = RELATIONSHIP
    data['solo'] = True

    session.close()

    return render(
        request, 'contact/modal.html', data
    )
