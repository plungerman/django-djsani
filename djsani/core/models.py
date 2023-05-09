# -*- coding: utf-8 -*-

"""Data models."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver
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
REZ_CHOICES = (
    ('M', 'Manager'),
    ('C', 'Commuter'),
    ('O', 'Off Campus'),
    ('R', 'Resident'),
)


def uploaded_email(sender, instance, manager, philes):
    """Send an email with data from model signal when student uploads file."""
    user = instance.user()
    if user and manager:
        to_list = []
        for trainer, sports in settings.UPLOAD_EMAIL_DICT.items():
            for spor in [sport.code for sport in manager.sports.all()]:
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
            previous = sender.objects.get(pk=instance.id)
            for phile in philes:
                if getattr(previous, phile, None).name != getattr(instance, phile, None):
                    philes[phile] = True
        user.debug = settings.DEBUG
        philes['user'] = user
        philes['server_url'] = settings.SERVER_URL
        philes['to_list'] = hidden_list
        for phile, status in philes.items():
            if isinstance(status, bool) and status:
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

        db_table = 'student_medical_content_type'

    def __repr__(self):
        """Default data for display."""
        return self.name


class StudentMedicalLogEntry(models.Model):
    """Audit trail logs."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

        db_table = 'student_medical_log_entry'

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


class Sport(models.Model):
    """Data class model for sports."""

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=4)
    status = models.BooleanField(default=True)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'athlete_sports'

    def __str__(self):
        """Default data for display."""
        return '{0} [{1}]'.format(self.name, self.code)


class StudentMedicalManager(models.Model):
    """Manager class for tracking meta data about other data models."""

    # core
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sitrep = models.BooleanField(null=True)
    sitrep_athlete = models.BooleanField(null=True)
    athlete = models.BooleanField(null=True)
    sports = models.ManyToManyField(Sport)
    concussion_baseline = models.BooleanField(null=True)
    medical_consent_agreement = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    medical_consent_agreement_status = models.BooleanField(null=True)
    covid19_vaccine_card = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    covid19_vaccine_card_status = models.BooleanField(null=True)
    physical_evaluation_1 = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    physical_evaluation_status_1 = models.BooleanField(null=True)
    physical_evaluation_2 = models.FileField(
        upload_to=upload_to_path,
        validators=FILE_VALIDATORS,
        max_length=128,
        null=True,
        blank=True,
    )
    physical_evaluation_status_2 = models.BooleanField(null=True)
    emergency_contact = models.BooleanField(null=True)
    # forms and waivers
    cc_student_immunization = models.BooleanField(null=True)
    cc_student_medical_history = models.BooleanField(null=True)
    cc_student_health_insurance = models.BooleanField(null=True)
    cc_student_meni_waiver = models.BooleanField(null=True)
    cc_athlete_medical_history = models.BooleanField(null=True)
    cc_athlete_privacy_waiver = models.BooleanField(null=True)
    cc_athlete_reporting_waiver = models.BooleanField(null=True)
    cc_athlete_risk_waiver = models.BooleanField(null=True)
    cc_athlete_sicklecell_waiver = models.BooleanField(null=True)
    staff_notes = models.TextField(null=True, blank=True)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'student_medical_manager'

    def __str__(self):
        """Default data for display."""
        user = self.user
        return user.username

    def current(self, day):
        """Determine if this is the current manager for academic year."""
        return self.created_at > day

    def get_slug(self):
        """Used for the upload_to_path helper for file uplaods."""
        return 'student-medical-manager'

    def get_meni(self):
        """Return current meni waiver"""
        return self.meni.filter(created_at__gte=settings.START_DATE).first()

    def get_privacy(self):
        """Return current privacy waiver"""
        return self.privacy.filter(created_at__gte=settings.START_DATE).first()

    def get_reporting(self):
        """Return current reporting waiver"""
        return self.reporting.filter(created_at__gte=settings.START_DATE).first()

    def get_risk(self):
        """Return current risk waiver"""
        return self.risk.filter(created_at__gte=settings.START_DATE).first()

    def get_sicklecell(self):
        """Return current risk waiver"""
        return self.sicklecell.filter(created_at__gte=settings.START_DATE).first()


class StudentProfile(models.Model):
    """Data class model for student data."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student',
    )
    second_name = models.CharField(max_length=255, null=True, blank=True)
    alt_name = models.CharField(max_length=255, null=True, blank=True)
    encrypted = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField("Date created", auto_now_add=True)
    updated_at = models.DateTimeField("Date updated", auto_now=True)
    expired_at = models.DateTimeField("Date updated", null=True, blank=True)
    status = models.BooleanField(default=True)
    birth_date = models.DateField(null=True, blank=True)
    adult = models.BooleanField(default=True)
    address1 = models.CharField("Address", max_length=128, null=True, blank=True)
    address2 = models.CharField("", max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.CharField("Zip code", max_length=10, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    gender = models.CharField(max_length=16, null=True, blank=True)
    class_year = models.CharField("Current Class", max_length=24, null=True, blank=True)
    residency = models.CharField(
        max_length=2,
        choices=REZ_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'student_profile'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def last_name(self):
        """Construct the link to the print view using the user's last name."""
        return self.user.last_name
    last_name.allow_tags = True
    last_name.short_description = "Sur Name"

    def first_name(self):
        """Construct the link to the default view using the user's first name."""
        return self.user.first_name
    first_name.allow_tags = True
    first_name.short_description = "Given Name"

    def username(self):
        """Construct the link to the default view using the user's username."""
        return self.user.username
    username.allow_tags = True
    username.short_description = "Username"

    def cid(self):
        """Construct the link to the default view using the user's ID."""
        return self.user.id
    cid.allow_tags = True
    cid.short_description = "CID"


@receiver(models.signals.pre_save, sender=StudentMedicalManager)
def uploaded_phile(sender, instance, **kwargs):
    """send an email if a student uploads a file."""
    if instance.id:
        philes = {
            'medical_consent_agreement': False,
            'physical_evaluation_1': False,
            'physical_evaluation_2': False,
        }
        uploaded_email(sender, instance, instance, philes)
