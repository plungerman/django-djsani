# -*- coding: utf-8 -*-

"""Forms for medical history."""

from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator
from djtools.fields import BINARY_CHOICES


SICKLE_CELL_RESULTS = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
)
DRUG_TEST_RESULTS = (
    ('No positive drug test', 'No positive drug test'),
    ('Positive drug test', 'Positive drug test'),
)
ALLOWED_IMAGE_EXTENSIONS = settings.ALLOWED_IMAGE_EXTENSIONS


class SicklecellForm(forms.Form):
    """Sickle Cell form."""

    results_file = forms.FileField(
        label="Results File",
        help_text="Photo/Scan of your test results",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS),
        ],
        required=True,
    )


class DopingForm(forms.Form):
    """Doping form."""

    part1 = forms.BooleanField(
        label="Statement Concerning Eligibility",
    )
    part2 = forms.BooleanField(
        label="Buckley Amendment Consent",
    )
    part3_1 = forms.BooleanField(
        label="Future positive test – all student-athletes sign",
    )
    part3_2 = forms.ChoiceField(
        label="Positive test by NCAA or other sports governing body",
        choices=DRUG_TEST_RESULTS,
        widget=forms.RadioSelect(),
    )
    part3_3 = forms.ChoiceField(
        label="Are you currently under such a drug-testing suspension?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )


class PrivacyForm(forms.Form):
    """Privacy waiver form."""

    news_media = forms.BooleanField(required=False)
    parents_guardians = forms.BooleanField(required=False)
    disclose_records = forms.BooleanField()


class ReportingForm(forms.Form):
    """Reporting requirements form."""

    agree = forms.BooleanField()


class RiskForm(forms.Form):
    """Assumption of risk form."""

    agree = forms.BooleanField()


class MeniForm(forms.Form):
    """Meningococcal Meningitis/Hepatitis B Response form."""

    agree = forms.BooleanField()
