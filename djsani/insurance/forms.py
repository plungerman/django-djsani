# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from djzbar.utils.informix import do_sql as do_esql
from djtools.fields import STATE_CHOICES, REQ_CSS
from djtools.utils.database import do_mysql
from localflavor.us.forms import USPhoneNumberField

POLICY_CHOICES = (
    ('', '---select---'),
    ('HMO', 'HMO'),
    ('PPO', 'PPO'),
    ('POS', 'POS'),
    ('State Insurance', 'State Insurance'),
    ('Other', 'Other'),
)

class StudentForm(forms.Form):
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
        help_text="Please provide the toll free customer service number",
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

    def __init__(self,*args,**kwargs):
        super(StudentForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = [
            'cid','created_at','updated_at','second_policy',
            'policy_holder','dob','company','phone',
            'member_id','group_no','policy_type','policy_state'
        ]

class AthleteForm(StudentForm):
    address = forms.CharField(
        label="Insurance address",
        widget=forms.Textarea,
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(AthleteForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = [
            'policy_holder','dob','company','phone',
            'address','member_id','group_no','policy_type','policy_state'
        ]

def _get_data(cid,fname):
    data = {}
    data["form1"] = {}
    data["form2"] = {}
    if not settings.DEBUG:
        sql = "select * from in student_insurance where cid = '%s'" % cid
        results = do_esql(sql, key=settings.INFORMIX_DEBUG)
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
