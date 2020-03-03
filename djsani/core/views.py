# -*- coding: utf-8 -*-

"""Views and helpers for the project as a whole."""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from djimix.decorators.auth import portal_auth_required
from djsani.core.models import CHANGE
from djsani.core.models import SPORTS
from djsani.core.models import SPORTS_MEN
from djsani.core.models import SPORTS_WOMEN
from djsani.core.models import StudentMedicalLogEntry
from djsani.core.models import StudentMedicalManager
from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_content_type
from djsani.core.utils import get_manager
from djsani.core.utils import get_term
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

from djmaidez.core.models import ENS_CODES
from djmaidez.core.models import ENS_FIELDS
from djmaidez.core.models import MOBILE_CARRIER
from djmaidez.core.models import RELATIONSHIP
from djzbar.utils.informix import get_engine
from djzbar.utils.informix import get_session


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
EARL = settings.INFORMIX_EARL


@csrf_exempt
@login_required
def set_val(request):
    """
    Ajax POST for to set a single name/value pair.

    Used mostly for jquery xeditable and ajax updates for
    student medical manager.

    Requires via POST:

    college_id
    name (database field)
    value
    pk (primary key of object to be updated)
    table
    """
    staff = in_group(request.user, settings.STAFF_GROUP)

    # we need a table name
    try:
        table = request.POST.get('table')
    except:
        table = None

    if not table:
        return HttpResponse("Error: no table name")
    # we need a college ID to insure no funny stuff
    cid = request.POST.get('college_id')
    if not cid:
        return HttpResponse("Error: no college ID")
    elif not staff and int(cid) != request.user.id:
        return HttpResponse("Not staff")
    else:
        # name/value pair
        name = request.POST.get('name')
        # sports field is a list
        if name == 'sports':
            value = ','.join(request.POST.getlist('value[]'))
        else:
            value = request.POST.get('value')

        # primary key
        pk = request.POST.get('pk')
        # create our dictionary to hold name/value pairs
        dic = { name: value }
        if table == 'cc_athlete_sicklecell_waiver':
            # set value = 1 if field name = 'waive'or
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
        # create database session
        session = get_session(EARL)
        # retrieve student manager
        man = get_manager(session, cid)

        if WAIVERS.get(table) and not pk:
            # create new waiver
            dic['college_id'] = cid
            dic['manager_id'] = man.id
            obj = WAIVERS[table](**dic)
            session.add(obj)
            # update the manager
            setattr(man, table, value)
            session.flush()
        else:
            model = BASES[table]
            obj = session.query(model).\
                filter_by(id=pk).first()
            if not obj:
                return HttpResponse(
                    "No object found associated with ID: {}".format(pk),
                    content_type='text/plain; charset=utf-8'
                )
            else:
                if name == 'athlete' and str(value) == '0':
                    dic['sports'] = ''

                # green check mark for athletes
                if name == 'sitrep_athlete' and str(value) == '1':
                    if obj.medical_consent_agreement:
                        dic['medical_consent_agreement_status'] = 1
                    if obj.physical_evaluation_1:
                        dic['physical_evaluation_status_1'] = 1
                    if obj.physical_evaluation_2:
                        dic['physical_evaluation_status_2'] = 1

                # update existing object
                for key, value in dic.iteritems():
                    setattr(obj, key, value)

                session.flush()
            # if waiver, update manager table
            if WAIVERS.get(table):
                setattr(man, table, value)

        # update the log entry for staff modifications
        if staff:
            message = ''
            for n, v in dic.items():
                message += '{0} = {1}\n'.format(n, v)
            log = {
                'college_id': request.user.id,
                'content_type_id': get_content_type(table).id,
                'object_id': obj.id,
                'object_repr': '{0}'.format(obj),
                'action_flag': CHANGE,
                'action_message': message,
            }
            log_entry = StudentMedicalLogEntry(**log)
            session.add(log_entry)

        session.commit()
        session.close()

        return HttpResponse(
            "success", content_type='text/plain; charset=utf-8',
        )


@portal_auth_required(
    session_var='DJSANI_AUTH', redirect_url=reverse_lazy('access_denied'),
)
def home(request):
    """Default home view when user signs in."""
    if settings.ACADEMIC_YEAR_LIMBO:
        return render(
            request, 'closed.html',
        )

    # for when faculty/staff sign in here or not student found
    context_data = {}
    # create database session
    session = get_session(EARL)
    user = request.user
    # fetch college id from user object
    cid = user.id
    # retrieve student manager (or create a new one if none exists)
    manager = get_manager(session, cid)
    # intialise some things
    my_sports = ''
    student = None
    adult = False
    # get academic term
    term = get_term()
    # get student
    sql = ''' {}
        WHERE
        id_rec.id = "{}"
        AND stu_serv_rec.yr = "{}"
        AND UPPER(stu_serv_rec.sess) = "{}"
        AND cc_student_medical_manager.created_at > "{}"
    '''.format(
        STUDENT_VITALS, cid, term['yr'], term['sess'], settings.START_DATE
    )
    engine = get_engine(EARL)
    obj = engine.execute(sql)
    student = obj.fetchone()
    if student:
        # save some things to Django session:
        request.session['gender'] = student.sex

        # sports needs a python list
        if manager.sports:
            my_sports = manager.sports.split(',')

        # adult or minor? if we do not have a DOB, default to minor
        if student.birth_date:
            age = calculate_age(student.birth_date)
            if age >= 18:
                adult = True

        # show the corresponding list of sports
        if student.sex == 'F':
            sports = SPORTS_WOMEN
        else:
            sports = SPORTS_MEN

        # quick switch for minor age students
        if request.GET.get('minor'):
            adult = False

        # context dict
        context_data = {
            'switch_earl': reverse_lazy('set_val'),
            'student':student,
            'manager':manager,
            'sports':sports,
            'my_sports':my_sports,
            'adult':adult,'sql':sql
        }

        # emergency contact modal form

        sql = 'SELECT * FROM aa_rec WHERE aa in {} AND id="{}"'.format(
            ENS_CODES, cid
        )
        objs = session.execute(sql)

        for o in objs:
            row = {}
            for field in ENS_FIELDS:
                try:
                    value = getattr(o, field).decode('cp1252').encode('utf-8')
                except Exception:
                    value = getattr(o, field)
                row[field] = value
            context_data[o.aa] = row
        context_data['mobile_carrier'] = MOBILE_CARRIER
        context_data['relationship'] = RELATIONSHIP
        context_data['solo'] = True
    else:
        # returns False if not student, which returns True
        facstaff = (
            not in_group(user, 'carthageStaffStatus') and
            not in_group(user, 'carthageFacultyStatus')
        )
        if facstaff:
            # could not find student by college_id
            context_data = {
                'student': student,
                'sports': SPORTS,
                'solo': True,
                'adult': adult,
            }
            # notify managers
            send_mail(
                request,
                settings.HOUSING_EMAIL_LIST,
                '[Lost] Student: {0} {1} ({2})'.format(
                    user.first_name, user.last_name, cid,
                ),
                user.email,
                'alert_email.html',
                request,
                [settings.MANAGERS[0][1]],
            )

    session.close()

    return render(request, 'home.html', context_data)


@csrf_exempt
@login_required
def rotate_photo(request):
    """AJAX Post request for rotating an image 90 degrees clockwise."""
    msg = "Error"
    phile = request.POST.get('phile')
    if phile:
        if phile.lower().split('.')[-1] in {'jpg', 'jpeg', 'png'}:
            path = '{0}/files/{1}'.format(settings.MEDIA_ROOT, phile)
            try:
                src_im = Image.open(path)
                im = src_im.rotate(90, expand=True)
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
