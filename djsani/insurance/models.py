# -*- coding: utf-8 -*-

"""Data models."""

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from djsani.core.models import StudentMedicalManager
from djsani.core.models import uploaded_email
from djtools.fields.helpers import upload_to_path


class StudentHealthInsurance(models.Model):
    """Student health insurance data, for both students and athletes."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(
        StudentMedicalManager,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    opt_out = models.BooleanField(null=True)
    # primary
    primary_policy_holder = models.CharField(max_length=128)
    primary_dob = models.DateField(null=True, blank=True)
    primary_company = models.CharField(max_length=128, null=True, blank=True)
    primary_phone = models.CharField(max_length=12, null=True, blank=True)
    primary_policy_address = models.CharField(max_length=255, null=True, blank=True)
    primary_member_id = models.CharField(max_length=64, null=True, blank=True)
    primary_group_no = models.CharField(max_length=64, null=True, blank=True)
    primary_policy_type = models.CharField(max_length=128, null=True, blank=True)
    primary_policy_state = models.CharField(max_length=2, null=True, blank=True)
    primary_card_front = models.FileField(
        upload_to=upload_to_path,
        max_length=128,
        null=True,
        blank=True,
    )
    primary_card_front_status = models.BooleanField(null=True)
    primary_card_back = models.FileField(
        upload_to=upload_to_path,
        max_length=128,
        null=True,
        blank=True,
    )
    primary_card_back_status = models.BooleanField(null=True)
    # secondary
    secondary_policy_holder = models.CharField(max_length=128, null=True, blank=True)
    secondary_dob = models.DateField(null=True, blank=True)
    secondary_company = models.CharField(max_length=128, null=True, blank=True)
    secondary_phone = models.CharField(max_length=12, null=True, blank=True)
    secondary_policy_address = models.CharField(max_length=255, null=True, blank=True)
    secondary_member_id = models.CharField(max_length=64, null=True, blank=True)
    secondary_group_no = models.CharField(max_length=64, null=True, blank=True)
    secondary_policy_type = models.CharField(max_length=128, null=True, blank=True)
    secondary_policy_state = models.CharField(max_length=2, null=True, blank=True)
    # tertiary
    tertiary_policy_holder = models.CharField(max_length=128, null=True, blank=True)
    tertiary_dob = models.DateField(null=True, blank=True)
    tertiary_company = models.CharField(max_length=128, null=True, blank=True)
    tertiary_phone = models.CharField(max_length=12, null=True, blank=True)
    tertiary_policy_address = models.CharField(max_length=255, null=True, blank=True)
    tertiary_member_id = models.CharField(max_length=64, null=True, blank=True)
    tertiary_group_no = models.CharField(max_length=64, null=True, blank=True)
    tertiary_policy_type = models.CharField(max_length=128, null=True, blank=True)
    tertiary_policy_state = models.CharField(max_length=2, null=True, blank=True)
    tertiary_card = models.FileField(
        upload_to=upload_to_path,
        max_length=128,
        null=True,
        blank=True,
    )

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'student_health_insurance'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def get_slug(self):
        """Used for the upload_to_path helper for file uplaods."""
        return 'insurance'

    def set_opt_out(self):
        """
        Empty the table when a student opts out.

        After a student has previously submitted insurance info we
        have to reset the values to an empty string.
        """
        for field in self._meta.fields:
            if field.name == 'opt_out':
                setattr(self, field.name, True)
            elif field.name not in {'manager', 'id', 'created_at'}:
                setattr(self, field.name, '')

    def current(self, day):
        """Determine if this is the current object for the academic year."""
        return self.created_at > day


#@receiver(models.signals.pre_save, sender=StudentHealthInsurance)
@receiver(models.signals.post_save, sender=StudentHealthInsurance)
def uploaded_phile(sender, instance, **kwargs):
    """send an email if a student uploads a file."""
    philes = {
        'primary_card_front': False,
        'primary_card_back': False,
        'tertiary_card': False,
    }
    uploaded_email(sender, instance, instance.manager, philes)
