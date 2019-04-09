# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator

from djtools.fields import STATE_CHOICES, REQ_CSS
from djtools.fields.localflavor import USPhoneNumberField

POLICY_CHOICES = (
    ('', '---select---'),
    ('HMO', 'HMO'),
    ('PPO', 'PPO'),
    ('POS', 'POS'),
    ('Gov', 'Medicaid'),
    ('Mil', 'Military'),
    ('Int', 'International')
)
ALLOWED_IMAGE_EXTENSIONS = settings.ALLOWED_IMAGE_EXTENSIONS


class AthleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop('manager', None)
        self.insurance = kwargs.pop('insurance', None)
        super(AthleteForm, self).__init__(*args, **kwargs)

    opt_out = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    primary_policy_holder = forms.CharField(
        label = "Policy holder",
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    primary_dob = forms.DateField(
        label = "Birth date (policy holder)",
        help_text="Format: mm/dd/yyyy",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required date'})
    )
    primary_company = forms.CharField(
        label = "Insurance company",
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    primary_phone = USPhoneNumberField(
        label = "Insurance phone number",
        max_length=12,
        help_text="Please provide the toll free customer service number",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required'})
    )
    primary_policy_address = forms.CharField(
        label="Insurance address",
        widget=forms.Textarea(),
        required=False,
    )
    primary_member_id = forms.CharField(
        label = "Member ID",
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    primary_group_no = forms.CharField(
        label = "Group number",
        max_length=64,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    primary_policy_type = forms.CharField(
        label="Type of policy",
        required=False,
        widget=forms.Select(choices=POLICY_CHOICES,attrs=REQ_CSS)
    )
    primary_policy_state = forms.CharField(
        label="If Medicaid, in which state?",
        widget=forms.Select(choices=STATE_CHOICES),
        required=False
    )
    primary_card_front = forms.FileField(
        label="Insurance Card Front",
        help_text="Photo/Scan of your insurance card",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)],
        required=False
    )
    primary_card_back = forms.FileField(
        label="Insurance Card Back",
        help_text="Photo/Scan of your insurance card",
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)],
        required=False
    )

    # secondary
    secondary_policy_holder = forms.CharField(
        label = "Policy holder",
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    secondary_dob = forms.DateField(
        label = "Birth date (policy holder)",
        help_text="Format: mm/dd/yyyy",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required date'})
    )
    secondary_company = forms.CharField(
        label = "Insurance company",
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    secondary_phone = USPhoneNumberField(
        label = "Insurance phone number",
        max_length=12,
        help_text="Please provide the toll free customer service number",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required phoneUS'})
    )
    secondary_policy_address = forms.CharField(
        label="Insurance address",
        widget=forms.Textarea(),
        required=False,
    )
    secondary_member_id = forms.CharField(
        label = "Member ID",
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    secondary_group_no = forms.CharField(
        label = "Group number",
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    secondary_policy_type = forms.CharField(
        label="Type of policy",
        required=False,
        widget=forms.Select(choices=POLICY_CHOICES,attrs=REQ_CSS)
    )
    secondary_policy_state = forms.CharField(
        label="If Medicaid, in which state?",
        widget=forms.Select(choices=STATE_CHOICES),
        required=False
    )

    # tertiary
    tertiary_policy_holder = forms.CharField(
        label = "Policy holder",
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    tertiary_dob = forms.DateField(
        label = "Birth date (policy holder)",
        help_text="Format: mm/dd/yyyy",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required date'})
    )
    tertiary_company = forms.CharField(
        label = "Insurance company",
        max_length=128,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    tertiary_phone = USPhoneNumberField(
        label = "Insurance phone number",
        max_length=12,
        help_text="Please provide the toll free customer service number",
        required=False,
        widget=forms.TextInput(attrs={'class': 'required phoneUS'})
    )
    tertiary_policy_address = forms.CharField(
        label="Insurance address",
        widget=forms.Textarea,
        required=False
    )
    tertiary_member_id = forms.CharField(
        label = "Member ID",
        max_length=64,
        required=False,widget=forms.TextInput(attrs=REQ_CSS)
    )
    tertiary_group_no = forms.CharField(
        label = "Group number",
        max_length=64,
        required=False,
        widget=forms.TextInput(attrs=REQ_CSS)
    )
    tertiary_policy_type = forms.CharField(
        label="Type of policy",
        required=False,
        widget=forms.Select(choices=POLICY_CHOICES,attrs=REQ_CSS)
    )
    tertiary_policy_state = forms.CharField(
        label="If Medicaid, in which state?",
        widget=forms.Select(choices=STATE_CHOICES),
        required=False
    )

    def clean(self):
        cd = self.cleaned_data
        insurance = self.insurance
        manager = self.manager
        if manager.athlete and not cd['opt_out']:
            if not cd.get('primary_card_front') or not cd.get('primary_card_back'):
                if not insurance:
                    error =  "Required Field"
                    self._errors['primary_card_front'] = self.error_class([error])
                    self._errors['primary_card_back'] = self.error_class([error])
        return self.cleaned_data


class StudentForm(AthleteForm):
    pass
