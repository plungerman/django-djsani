# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from djzbar.utils.informix import do_sql
from djtools.fields import STATE_CHOICES, REQ_CSS

from localflavor.us.forms import USPhoneNumberField

POLICY_CHOICES = (
    ('', '---select---'),
    ('HMO', 'HMO'),
    ('PPO', 'PPO'),
    ('POS', 'POS'),
    ('State Insurance', 'State Insurance'),
    ('Other', 'Other'),
)

class AcademicsForm(forms.Form):
    policy_holder = forms.CharField(
        max_length=128,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    dob = forms.DateField(
        label = "Birth date (policy holder)",
        help_text="Format: mm/dd/yyyy",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required date'})
    )
    company = forms.CharField(
        label = "Insurance company",
        max_length=128,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    phone = USPhoneNumberField(
        label = "Insurance phone number",
        max_length=12,
        help_text="Please provide a toll free number",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required phoneUS'})
    )
    member_id = forms.CharField(
        label = "Member ID",
        max_length=64,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    group_no = forms.CharField(
        label = "Group number",
        max_length=64,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    policy_type = forms.CharField(
        label="Type of policy",
        required=False,
        widget=forms.Select(choices=POLICY_CHOICES,attrs=REQ_CSS)
    )
    policy_state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES),
        required=False
    )

class AthleticsForm(AcademicsForm):
    address = forms.CharField(
        label="Insurance address",
        widget=forms.Textarea,
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(AthleticsForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = [
            'policy_holder','dob','company','phone',
            'address','member_id','group_no','policy_type','policy_state'
        ]

def _put_data(forms,status=0):
    # we pass 'status' to this method which is the
    # len() of the data set returned from informix
    # via the _get_data() method.
    if status==1:
        prefix = "update student_insurance"
    else:
        prefix = "insert into student_insurance"
    if not forms[0]:
        # opt out: set all values to null/''
        # set opt_out to True/1
        sql = "%s " % prefix
    elif not forms[1]:
        # no secondary: set secondary_* values to null/''
        sql = "%s " % prefix
    else:
        # primary and secondary
        # set secondary to True/1
        sql = "%s " % prefix
    if not settings.DEBUG:
        do_sql(sql, key=settings.INFORMIX_DEBUG)

def _get_data(cid,fname):
    data = {}
    data["form1"] = {}
    data["form2"] = {}
    if not settings.DEBUG:
        sql = "select * from in student_insurance where cid = '%s'" % cid
        results = do_sql(sql, key=settings.INFORMIX_DEBUG)
        obj = results.fetchall()
        # if len() == 0, insert; if len() == 1, update
        data["status"] = len(obj)
        # dictionaries to populate forms on GET
        if data["status"] == 1:
            form = eval(fname)()
            for f in form.field:
                data["form1"][f] = obj["primary_%s"] % f
                data["form2"][f] = obj["secondary_%s"] % f
            data["opt-out"] = obj.opt_out
            data["secondary"] = obj.secondary
    else:
        data["status"] = 0
    return data
