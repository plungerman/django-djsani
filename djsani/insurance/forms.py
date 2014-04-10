# -*- coding: utf-8 -*-

from django import forms

from djtools.fields import BINARY_CHOICES

from localflavor.us.forms import USPhoneNumberField

POLICY_CHOICES = (
    ('HMO', 'HMO'),
    ('PPO', 'PPO'),
    ('EPO', 'EPO'),
    ('POS', 'POS'),
)

class InsuranceForm(forms.Form):
    primary = forms.ChoiceField(
        label="Is this your primary Insurance Policy?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect()
    )
    policy_holder = forms.CharField(
        max_length=128,
        required=False
    )
    dob = forms.DateField(
        label = "Birth date (policy holder)",
        help_text="Format: mm/dd/yyyy",
        required=False
    )
    insurance_company = forms.CharField(
        max_length=128,
        required=False
    )
    insurance_phone = USPhoneNumberField(
        max_length=12,
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
        label="Type of policy?",
        choices=POLICY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )

