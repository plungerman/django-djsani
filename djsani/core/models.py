# -*- coding: utf-8 -*-

"""Data models."""

import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djsani.core.sql import SPORTS_STUDENT
from djtools.fields.helpers import upload_to_path
from djtools.utils.mail import send_mail


ALLOWED_EXTENSIONS = (
    'xls', 'xlsx', 'doc', 'docx', 'pdf', 'txt', 'png', 'jpg', 'jpeg', 'heic',
)
FILE_VALIDATORS = [
    FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS),
]
ADDITION = 1
CHANGE = 2
DELETION = 3


def uploaded_email(sender, instance, philes):
    """Send an email with data from model signal when student uploads file."""
    user = instance.user()
    to_list = []
    try:
        manager = instance.manager
    except Exception:
        manager = instance
    for trainer, sports in settings.UPLOAD_EMAIL_DICT.items():
        for spor in [sport.sport_code for sport in manager.sports()]:
            if spor in sports and trainer not in to_list:
                to_list.append(trainer)
    hidden_list = to_list
    if settings.DEBUG:
        to_list = [settings.SERVER_EMAIL]

    if instance.id is None:
        for phile in philes:
            if getattr(instance, phile, None):
                philes[phile] = True
    else:
        previous = sender.objects.using('informix').get(pk=instance.id)
        for phile in philes:
            if getattr(previous, phile, None).name != getattr(instance, phile, None):
                philes[phile] = True
    user.debug = settings.DEBUG
    philes['user'] = user
    philes['server_url'] = settings.SERVER_URL
    philes['to_list'] = hidden_list
    for phile, status in philes.items():
        if isinstance(status, bool) and status:
            logger = logging.getLogger('phile={0}'.format(phile))
            logger = logging.getLogger('status={0}'.format(status))
            send_mail(
                None,
                to_list,
                '[File Uploaded] {0}, {1} ({2})'.format(
                    user.last_name,
                    user.first_name,
                    user.id,
                ),
                user.email,
                'upload_email.html',
                philes,
                [settings.MANAGERS[0][1]],
            )
            break


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
    concussion_baseline = models.BooleanField()
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
        return str(self.college_id)

    def current(self, day):
        """Determine if this is the current manager for academic year."""
        return self.created_at > day

    def get_slug(self):
        """Used for the upload_to_path helper for file uplaods."""
        return 'student-medical-manager'

    def user(self):
        """Obtain the system user for student."""
        try:
            user = User.objects.get(pk=self.college_id)
        except Exception:
            user = None
        return user

    def sports(self):
        """Obtain the sports for a student or all the sports."""
        # sports end_date is always around mid-may so a manager created
        # in august would correspond to an end_date in the following year,
        # while a manager created in january or february would correspond
        # to an end_date in the current year.
        date = self.created_at
        if date.month < settings.SPORTS_MONTH:
            year = date.year
        else:
            year = date.year + 1
        sql = SPORTS_STUDENT(cid=self.college_id, year=year)
        with get_connection() as connection:
            return xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchall()


@receiver(models.signals.pre_save, sender=StudentMedicalManager)
def uploaded_phile(sender, instance, **kwargs):
    """send an email if a student uploads a file."""
    philes = {
        'medical_consent_agreement': False,
        'physical_evaluation_1': False,
        'physical_evaluation_2': False,
    }
    uploaded_email(sender, instance, philes)
