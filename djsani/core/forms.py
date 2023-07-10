# -*- coding: utf-8 -*-

"""Forms for the student medical manager."""

from django import forms
from django.conf import settings
from djsani.core.models import Sport
from djsani.core.models import StudentMedicalManager


class SportForm(forms.ModelForm):
    """Sports form for student athletes."""

    sports = forms.ModelMultipleChoiceField(
        label="",
        queryset=Sport.objects.filter(status=True),
        help_text='Check all that apply',
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        """Attributes about the form class."""

        model = StudentMedicalManager
        fields = ['sports']
