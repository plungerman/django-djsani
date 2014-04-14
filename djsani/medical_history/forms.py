# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from djtools.fields import BINARY_CHOICES
from djzbar.utils.informix import do_sql

CHOICES = (
    ('', ''),
)

class AcademicsForm(forms.Form):
    holder = forms.CharField(
        label="",
        max_length=128,
        required=False
    )
    date = forms.DateField(
        help_text="Format: mm/dd/yyyy",
        required=False
    )
    choice = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )

class AthleticsForm(AcademicsForm):
    text = forms.CharField(
        widget=forms.Textarea
    )

    def __init__(self,*args,**kwargs):
        super(AthleticsForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = []

def _put_data(forms,status=0):
    # we pass 'status' to this method which is the
    # len() of the data set returned from informix
    # via the _get_data() method.
    if status==1:
        prefix = "update student_medical_history"
    else:
        prefix = "insert into student_medical_history"
    sql = "%s " % prefix
    do_sql(sql, key=settings.INFORMIX_DEBUG)

def _get_data(cid,fname):
    data = {}
    # dictionary to populate form on GET
    """
    data["form"] = {}
    sql = "select * from in student_medical_history where cid = '%s'" % cid
    results = do_sql(sql, key=settings.INFORMIX_DEBUG)
    obj = results.fetchall()
    # if len() == 0, insert; if len() == 1, update
    data["status"] = len(obj)
    if data["status"] == 1:
        form = eval(fname)()
        for f in form.field:
            data["form"][f] = obj["%s"] % f
    """
    return data
