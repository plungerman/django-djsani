from django.conf import settings
from djzbar.utils.informix import get_session
from djsani.core.utils import get_manager

EARL = settings.INFORMIX_EARL
session = get_session(EARL)

cid =
obj = get_manager(session,cid)

print obj.__dict__
print obj.status
