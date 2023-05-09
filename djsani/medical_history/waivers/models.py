# -*- coding: utf-8 -*-

"""Data models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from djsani.core.models import FILE_VALIDATORS
from djsani.core.models import StudentMedicalManager
from djsani.core.models import uploaded_email
from djtools.fields.helpers import upload_to_path


class Sicklecell(models.Model):
    """Sicklecell waiver."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    manager = models.ForeignKey(
        StudentMedicalManager,
        on_delete=models.CASCADE,
        related_name='sicklecell',
        db_constraint=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    waive = models.BooleanField(null=True)
    proof = models.BooleanField(null=True)
    # remove after migration
    results = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    results_file = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    results_file_status = models.BooleanField(null=True)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'athlete_sicklecell_waiver'

    def __str__(self):
        """Default value for this object."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day

    def get_slug(self):
        """Used for the upload_to_path helper for file uplaods."""
        return 'sicklecell'


class Meni(models.Model):
    """Meningitis and Hepatitis B waiver."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    manager = models.ForeignKey(
        StudentMedicalManager,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='meni',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    agree = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'student_meni_waiver'

    def __str__(self):
        """Default value for this object."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Risk(models.Model):
    """Assumption of Risk Waiver."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    manager = models.ForeignKey(
        StudentMedicalManager,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='risk',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    agree = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'athlete_risk_waiver'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Reporting(models.Model):
    """CCIW Injury and Illness Reporting Acknowledgement."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    manager = models.ForeignKey(
        StudentMedicalManager,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='reporting',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    agree = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'athlete_reporting_waiver'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Privacy(models.Model):
    """Privacy waiver."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    manager = models.ForeignKey(
        StudentMedicalManager,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='privacy',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    news_media = models.BooleanField(null=True)  # not required
    medical_insurance = models.BooleanField(null=True)  # not required
    ncaa_tool = models.BooleanField(null=True)  # not required
    parents_guardians = models.BooleanField(null=True)  # not required
    disclose_records = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'athlete_privacy_waiver'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


@receiver(models.signals.post_save, sender=Sicklecell)
def uploaded_phile(sender, instance, **kwargs):
    """send an email if a student uploads a file."""
    philes = {'results_file': True}
    manager = StudentMedicalManager.objects.filter(
        user=instance.user,
    ).filter(created_at__gte=settings.START_DATE).first()
    uploaded_email(sender, instance, manager, philes)
