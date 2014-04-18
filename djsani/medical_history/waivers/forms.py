# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from djzbar.utils.informix import do_sql

class SickleForm(forms.Form):
    waive = forms.BooleanField(
        required=False
    )
    proof = forms.BooleanField(
        required=False
    )

    def clean(self):
        """
        User must choose one or the other of two checkboxes.
        """
        cleaned_data = self.cleaned_data

        if not cleaned_data["waive"] and not cleaned_data["proof"]:
            raise forms.ValidationError(
                "Please check one of the checkboxes below."
            )
        return cleaned_data

class PrivacyForm(forms.Form):
    ncaa_tool = forms.BooleanField(
        required=False
    )
    medical_insurance = forms.BooleanField(
        required=False
    )
    news_media = forms.BooleanField(
        required=False
    )
    parents_guardians = forms.BooleanField(
        required=False
    )
    disclose_records = forms.BooleanField(
        required=False
    )

class ReportingForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )

class RiskForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )

def _put_data(forms,status=0):
    # we pass 'status' to this method which is the
    # len() of the data set returned from informix
    # via the _get_data() method.
    if status==1:
        prefix = "update student_medical_history"
    else:
        prefix = "insert into student_medical_history"
    sql = "%s " % prefix
    if not settings.DEBUG:
        do_sql(sql, key=settings.INFORMIX_DEBUG)

def _get_data(cid,fname):
    data = {}
    # dictionary to populate form on GET
    data["form"] = {}
    if not settings.DEBUG:
        sql = "select * from in student_medical_history where cid = '%s'" % cid
        results = do_sql(sql, key=settings.INFORMIX_DEBUG)
        obj = results.fetchall()
        # if len() == 0, insert; if len() == 1, update
        data["status"] = len(obj)
        if data["status"] == 1:
            form = eval(fname)()
            for f in form.field:
                data["form"][f] = obj["%s"] % f
    else:
        data["status"] = 0
    return data
