# -*- coding: utf-8 -*-

"""Data models."""

from django.core.validators import FileExtensionValidator
from django.db import models
from djtools.fields.helpers import upload_to_path


ALLOWED_EXTENSIONS = (
    'xls', 'xlsx', 'doc', 'docx', 'pdf', 'txt', 'png', 'jpg', 'jpeg',
)
FILE_VALIDATORS = [
    FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
]
ADDITION = 1
CHANGE = 2
DELETION = 3


class StudentMedicalContentType(models.Model):
    """Content types for the data models."""

    name = models.CharField(max_length=200)
    app_label = models.CharField(max_length=200)
    model = models.CharField(max_length=200)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_student_medical_content_type'

    def __repr__(self):
        """Default data for display."""
        return self.name


class StudentMedicalLogEntry(models.Model):
    """Audit trail logs."""

    college_id = models.IntegerField()
    action_time = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(
        StudentMedicalContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.IntegerField()
    object_repr = models.CharField(max_length=255)
    action_flag = models.PositiveSmallIntegerField()
    action_message = models.TextField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_student_medical_log_entry'

    def __repr__(self):
        """Default data for display."""
        if self.action_flag == ADDITION:
            return ('Added "{0}".'.format(self.object_repr))
        elif self.action_flag == CHANGE:
            return ('Changed "{0}" - {1}'.format(
                self.object_repr, self.change_message,
            ))
        elif self.action_flag == DELETION:
            return ('Deleted "{0}."'.format(self.object_repr))

        return 'LogEntry Object'

    def is_addition(self):
        """Check if the action is new."""
        return self.action_flag == ADDITION

    def is_change(self):
        """Check if the action is an update."""
        return self.action_flag == CHANGE

    def is_deletion(self):
        """Check if the action is a deletion."""
        return self.action_flag == DELETION


class StudentMedicalManager(models.Model):
    """Manager class for tracking meta data about other data models."""

    # core
    college_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    sitrep = models.BooleanField()
    sitrep_athlete = models.BooleanField()
    athlete = models.BooleanField()
    concussion_baseline = models.BooleanField()
    sports = models.CharField(max_length=255, null=True, blank=True)
    medical_consent_agreement = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    medical_consent_agreement_status = models.BooleanField()
    physical_evaluation_1 = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    physical_evaluation_status_1 = models.BooleanField()
    physical_evaluation_2 = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    physical_evaluation_status_2 = models.BooleanField()
    emergency_contact = models.BooleanField()
    # forms and waivers
    cc_student_immunization = models.BooleanField()
    cc_student_medical_history = models.BooleanField()
    cc_student_health_insurance = models.BooleanField()
    cc_student_meni_waiver = models.BooleanField()
    cc_athlete_medical_history = models.BooleanField()
    cc_athlete_privacy_waiver = models.BooleanField()
    cc_athlete_reporting_waiver = models.BooleanField()
    cc_athlete_risk_waiver = models.BooleanField()
    cc_athlete_sicklecell_waiver = models.BooleanField()
    staff_notes = models.TextField()

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_student_medical_manager'

    def __repr__(self):
        """Default data for display."""
        return self.college_id

    def current(self, day):
        """Determine if this is the current manager for academic year."""
        return self.created_at > day

    def get_slug(self):
        """Used for the upload_to_path helper for file uplaods."""
        return 'student-medical-manager'


# IDs must be unique pattern that does not repeat in any other
# item e.g 25 & 250 will not work.
SPORTS_MEN = (
    ('0', "----Men's Sport----"),
    ('15', 'Baseball'),
    ('25', 'Basketball'),
    ('35', 'Cross Country'),
    ('45', 'Football'),
    ('55', 'Golf'),
    ('61', 'Ice Hockey'),
    ('65', 'Lacrosse'),
    ('75', 'Soccer'),
    ('85', 'Swimming'),
    ('95', 'Tennis'),
    ('105', 'Track &amp; Field'),
    ('120', 'Volleyball'),
)
SPORTS_WOMEN = (
    ('0', "----Women's Sports----"),
    ('200', 'Basketball'),
    ('210', 'Cross Country'),
    ('220', 'Golf'),
    ('225', 'Ice Hockey'),
    ('230', 'Lacrosse'),
    ('240', 'Soccer'),
    ('260', 'Softball'),
    ('270', 'Swimming'),
    ('280', 'Tennis'),
    ('290', 'Track &amp; Field'),
    ('300', 'Volleyball'),
    ('305', 'Water Polo'),
)

SPORTS = SPORTS_WOMEN + SPORTS_MEN
