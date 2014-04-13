# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from djzbar.utils.informix import do_sql

from localflavor.us.forms import USPhoneNumberField

POLICY_CHOICES = (
    ('HMO', 'HMO'),
    ('PPO', 'PPO'),
    ('EPO', 'EPO'),
    ('POS', 'POS'),
)

class AcademicsForm(forms.Form):
    policy_holder = forms.CharField(
        max_length=128,
        required=False
    )
    dob = forms.DateField(
        label = "Birth date (policy holder)",
        help_text="Format: mm/dd/yyyy",
        required=False
    )
    company = forms.CharField(
        label = "Insurance company",
        max_length=128,
        required=False
    )
    phone = USPhoneNumberField(
        label = "Insurance phone number",
        max_length=12,
        help_text="Please provide a toll free number",
        required=False
    )
    member_id = forms.CharField(
        label = "Member ID",
        max_length=64,
        required=False
    )
    group_no = forms.CharField(
        label = "Group number",
        max_length=64,
        required=False
    )
    policy_type = forms.ChoiceField(
        label="Type of policy",
        choices=POLICY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )

class AthleticsForm(AcademicsForm):
    address = forms.CharField(
        label="Insurance address",
        widget=forms.Textarea
    )

    def __init__(self,*args,**kwargs):
        super(AthleticsForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = [
            'policy_holder','dob','company','phone',
            'address','member_id','group_no','policy_type'
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
        sql = "%s " % prefix
    elif not forms[1]:
        # no secondary: set secondary to null/''
        sql = "%s " % prefix
    else:
        # primary and secondary
        sql = "%s " % prefix
    do_sql(sql)

def _get_data(cid,fname):
    data = {}
    data["form1"] = {}
    data["form2"] = {}
    """
    sql = "select * from in student_insurance where cid = '%s'" % cid
    results = do_sql(sql, key=settings.INFORMIX_DEBUG)
    obj = results.fetchall()
    # if len() == 0, insert; if len() == 1, update
    data["status"] = len(obj)
    # dictionaries to populate forms on GET
    if data["status"] == 1:
        form = eval(fname)()
        for f in form.field:
            data["form1"][f] = obj["primary-%s"] % f
            data["form2"][f] = obj["secondary-%s"] % f
        data["opt-out"] = obj.opt_out
    """
    return data
