from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from djsani.core.sql import STUDENT_VITALS
from djsani.core.utils import get_content_type, get_manager, get_term

from djsani.core.models import SPORTS_WOMEN, SPORTS_MEN, SPORTS
from djsani.core.models import StudentMedicalManager
from djsani.core.models import StudentMedicalLogEntry
from djsani.core.models import ADDITION, CHANGE
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.waivers.models import Meni, Privacy, Reporting
from djsani.medical_history.waivers.models import Risk, Sicklecell
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory

from djmaidez.core.models import (
    ENS_CODES, ENS_FIELDS, MOBILE_CARRIER, RELATIONSHIP
)
from djzbar.utils.informix import get_engine, get_session
from djzbar.decorators.auth import portal_auth_required
from djtools.utils.date import calculate_age
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djtools.fields import TODAY

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
EARL = settings.INFORMIX_EARL


@csrf_exempt
@login_required
def set_val(request):
    """
    Ajax POST for to set a single name/value pair, used mostly for
    jquery xeditable and ajax updates for student medical manager.

    Requires via POST:

    college_id
    name (database field)
    value
    pk (primary key of object to be updated)
    table
    """

    staff = in_group(request.user, settings.STAFF_GROUP)

    # we need a table name
    table = request.POST.get('table')
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
            for n,v in dic.items():
                message += u'{} = {}\n'.format(n,v)
            log = {
                'college_id': request.user.id,
                'content_type_id': get_content_type(session, table).id,
                'object_id': obj.id,
                'object_repr': '{}'.format(obj),
                'action_flag': CHANGE,
                'action_message': message
            }
            log_entry = StudentMedicalLogEntry(**log)
            session.add(log_entry)

        session.commit()
        session.close()

        return HttpResponse(
            "success", content_type='text/plain; charset=utf-8'
        )


@portal_auth_required(
    session_var='DJSANI_AUTH', redirect_url=reverse_lazy('access_denied')
)
def home(request):
    if settings.ACADEMIC_YEAR_LIMBO:
        return render(
            request, 'closed.html',
        )

    # for when faculty/staff sign in here or not student found
    data = {}
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
        data = {
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
                except:
                    value = getattr(o, field)
                row[field] = value
            data[o.aa] = row
        data['mobile_carrier'] = MOBILE_CARRIER
        data['relationship'] = RELATIONSHIP
        data['solo'] = True
    else:
        if not in_group(user, 'carthageStaffStatus') and \
          not in_group(user, 'carthageFacultyStatus'):
            # could not find student by college_id
            data = {
                'student':student,'sports':SPORTS,'solo':True,'adult':adult
            }
            # notify managers
            send_mail(
                request, settings.HOUSING_EMAIL_LIST,
                u'[Lost] Student: {} {} ({})'.format(
                    user.first_name, user.last_name, cid
                ), user.email, 'alert_email.html', request,
                [settings.MANAGERS[0][1],]
            )

    session.close()

    return render(request, 'home.html', data)


@csrf_exempt
@login_required
def rotate_photo(request):
    '''
    AJAX Post request for rotating an image 90 degrees clockwise
    '''
    msg = "Error"
    phile = request.POST.get('phile')
    if phile:
        if phile.lower().split('.')[-1] in ['jpg','jpeg','png']:
            path = '{}/files/{}'.format(settings.MEDIA_ROOT,phile)
            try:
                src_im = Image.open(path)
                im = src_im.rotate(90, expand=True)
                im.save(path)
                msg = "Success"
            except:
                msg = "Something is a miss with that file."
        else:
            msg = "The file is not a graphics file."

    return HttpResponse(
        msg, content_type='text/plain; charset=utf-8'
    )

def responsive_switch(request,action):
    if action=='go':
        request.session['desktop_mode']=True
    elif action=='leave':
        request.session['desktop_mode']=False
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))
