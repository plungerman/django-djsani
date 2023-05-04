# -*- coding: utf-8 -*-

"""Views and helpers for the project as a whole."""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from djsani.core.models import CHANGE
from djsani.core.models import StudentMedicalLogEntry
from djsani.core.models import StudentMedicalManager
from djsani.core.utils import get_content_type
from djsani.core.utils import get_manager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Meni
from djsani.medical_history.waivers.models import Privacy
from djsani.medical_history.waivers.models import Reporting
from djsani.medical_history.waivers.models import Risk
from djsani.medical_history.waivers.models import Sicklecell
from djtools.utils.date import calculate_age
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from PIL import Image


# table names are the key, base model classes are the value

WAIVERS = {
    'cc_student_meni_waiver': Meni,
    'cc_athlete_privacy_waiver': Privacy,
    'cc_athlete_reporting_waiver': Reporting,
    'cc_athlete_risk_waiver': Risk,
    'cc_athlete_sicklecell_waiver': Sicklecell,
}
BASES = {
    'cc_student_medical_manager': StudentMedicalManager,
    'cc_student_health_insurance': StudentHealthInsurance,
    'cc_student_medical_history': StudentMedicalHistory,
    'cc_athlete_medical_history': AthleteMedicalHistory,
}
BASES.update(WAIVERS)


@csrf_exempt
@login_required
def set_val(request):
    """
    Ajax POST to set a single name/value pair.

    Used mostly for jquery xeditable and ajax updates for
    student medical manager.

    Requires via POST:

    college_id
    name (database field)
    value
    pk (primary key of object to be updated)
    table
    """
    user = request.user
    staff = in_group(user, settings.STAFF_GROUP)
    # college ID
    cid = request.POST.get('college_id')
    # name/value pair
    name = request.POST.get('name')
    # primary key
    pk = request.POST.get('pk')
    # table name
    table = request.POST.get('table')
    # value
    value = request.POST.get('value')
    if not cid or not name or not table or not value:
        return HttpResponse("Missing required parameters.")
    if not staff and int(cid) != user.id:
        return HttpResponse("Not staff")
    else:
        # create our dictionary to hold name/value pairs
        dic = {name: value}
        if table == 'cc_athlete_sicklecell_waiver':
            # set value = 1 if field name = 'waive' or
            # if it = 'results' since that value is
            # either Positive or Negative
            if name == 'results':
                dic['proof'] = 1
                dic['waive'] = 0
                value = 1
            elif name == 'waive':
                dic['proof'] = 0
                dic['waive'] = value
                dic['results'] = ''
            elif name == 'proof':
                dic['results'] = ''
        # retrieve student manager
        manager = get_manager(cid)
        if WAIVERS.get(table) and not pk:
            # create new waiver
            dic['college_id'] = cid
            dic['manager_id'] = manager.id
            nobj = WAIVERS[table](**dic)
            nobj.save()
            # update the manager
            setattr(manager, table, value)
            manager.save()
        else:
            model = BASES[table]
            nobj = model.objects.filter(pk=pk).first()
            if nobj:
                # green check mark for athletes
                if name == 'sitrep_athlete' and str(value) == '1':
                    if nobj.medical_consent_agreement:
                        dic['medical_consent_agreement_status'] = 1
                    if nobj.physical_evaluation_1:
                        dic['physical_evaluation_status_1'] = 1
                    if nobj.physical_evaluation_2:
                        dic['physical_evaluation_status_2'] = 1
                # update existing object
                for key, dic_val in dic.items():
                    setattr(nobj, key, dic_val)
                nobj.save()
            else:
                return HttpResponse(
                    "No object found associated with ID: {0}".format(pk),
                    content_type='text/plain; charset=utf-8',
                )
            # if waiver, update manager table
            if WAIVERS.get(table):
                setattr(manager, table, value)
                manager.save()

        # update the log entry for staff modifications
        if staff:
            message = ''
            for dkey, dval in dic.items():
                message += '{0} = {1}\n'.format(dkey, dval)
            log = StudentMedicalLogEntry(
                college_id=user.id,
                content_type_id=get_content_type(table).id,
                object_id=nobj.id,
                object_repr=nobj,
                action_flag=CHANGE,
                action_message=message,
            )
            log.save()

        return HttpResponse(name, content_type='text/plain; charset=utf-8')


@login_required
def home(request):
    """Default home view when user signs in."""
    if settings.ACADEMIC_YEAR_LIMBO:
        return render(
            request, 'closed.html',
        )
    # for when faculty/staff sign in here or not student found
    context_data = {}
    # set our user
    user = request.user
    # staff or coach?
    staff = in_group(user, settings.STAFF_GROUP)
    coach = in_group(user, settings.COACH_GROUP)
    student = in_group(user, settings.STUDENT_GROUP)
    if student:
        # retrieve student manager (or create a new one if none exists)
        manager = get_manager(user.id)
        context_data = {
            'switch_earl': reverse_lazy('set_val'),
            'student': student,
            'manager': manager,
        }
    else:
        context_data['staff'] = staff
        context_data['coach'] = coach

    return render(request, 'home.html', context_data)


@csrf_exempt
def rotate_photo(request):
    """AJAX Post request for rotating an image 90 degrees clockwise."""
    msg = "Error"
    phile = request.POST.get('phile')
    if phile:
        if phile.lower().split('.')[-1] in {'jpg', 'jpeg', 'png'}:
            path = '{0}/files/{1}'.format(settings.MEDIA_ROOT, phile)
            try:
                src_im = Image.open(path)
                im = src_im.rotate(settings.ROTATE_PHOTO, expand=True)
                im.save(path)
                msg = "Success"
            except Exception:
                msg = "Something is a miss with that file."
        else:
            msg = "The file is not a graphics file."

    return HttpResponse(
        msg, content_type='text/plain; charset=utf-8',
    )


def responsive_switch(request, action):
    """Switch between desktop and responsive UI."""
    if action == 'go':
        request.session['desktop_mode'] = True
    elif action == 'leave':
        request.session['desktop_mode'] = False
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))
