# -*- coding: utf-8 -*-

"""Data models."""

from django.db import models
from djsani.core.models import FILE_VALIDATORS
from djtools.fields.helpers import upload_to_path


class Sicklecell(models.Model):
    """Sicklecell waiver."""

    # core
    college_id = models.IntegerField()
    manager_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # waiver fields
    waive = models.BooleanField()
    proof = models.BooleanField()
    results = models.CharField(max_length=64)
    results_file = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    results_file_status = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_athlete_sicklecell_waiver'

    def __repr__(self):
        """Default value for this object."""
        return self.college_id

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Meni(models.Model):
    """Meningitis and Hepatitis B waiver."""

    # core
    college_id = models.IntegerField()
    manager_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # waiver fields
    agree = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_student_meni_waiver'

    def __repr__(self):
        """Default value for this object."""
        return self.college_id

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Risk(models.Model):
    """Assumption of Risk Waiver."""

    # core
    college_id = models.IntegerField()
    manager_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    agree = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_athlete_risk_waiver'

    def __repr__(self):
        """Default data for display."""
        return self.college_id

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Reporting(models.Model):
    """CCIW Injury and Illness Reporting Acknowledgement."""

    # core
    college_id = models.IntegerField()
    manager_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    agree = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_athlete_reporting_waiver'

    def __repr__(self):
        """Default data for display."""
        return self.college_id

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day


class Privacy(models.Model):
    """Privacy waiver."""

    # core
    college_id = models.IntegerField()
    manager_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    # waiver fields
    news_media = models.BooleanField()  # not required
    parents_guardians = models.BooleanField()  # not required
    disclose_records = models.BooleanField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_athlete_privacy_waiver'

    def __repr__(self):
        """Default data for display."""
        return self.college_id

    def current(self, day):
        """Determine if this is the current waiver for academic year."""
        return self.created_at > day
