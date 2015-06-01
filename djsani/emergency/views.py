from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext, loader

from djsani.emergency.models import AARec

from djtools.utils.database import row2dict
from djzbar.utils.informix import do_sql, get_session
from djmaidez.core.models import ENS_CODES, MOBILE_CARRIER, RELATIONSHIP

EARL = settings.INFORMIX_EARL

@login_required
def emergency_contact(request):
    """
    Emergency contact modal generator
    """
    cid = request.GET.get("UserID", "")

    session = get_session(EARL)

    objs = session.query(AARec).filter_by(id=cid).\
        filter(AARec.aa.in_(ENS_CODES)).all()

    data = {}
    for o in objs:
        data[o.aa] = row2dict(o)
    data["mobile_carrier"] = MOBILE_CARRIER
    data["relationship"] = RELATIONSHIP
    data["solo"] = True

    session.close()

    return render_to_response(
        "contact/modal.html", data,
        context_instance=RequestContext(request)
    )
