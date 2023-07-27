# -*- coding: utf-8 -*-

"""Data models."""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from djsani.core.models import StudentMedicalManager
from djtools.utils.mail import send_mail


class StudentMedicalHistory(models.Model):
    """Student Medical History data model."""

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
    # medical history fields
    covid19_positive = models.TextField(null=True)
    covid19_vacination = models.TextField(null=True)
    allergies_medical = models.TextField(null=True)
    allergies_other = models.TextField(null=True)
    anemia = models.TextField(null=True)
    bronchospasm = models.TextField(null=True)
    birth_defect = models.TextField(null=True)
    blood_disorder = models.TextField(null=True)
    bronchitis = models.TextField(null=True)
    cancer = models.TextField(null=True)
    chicken_pox = models.TextField(null=True)
    diabetes = models.TextField(null=True)
    ent_disorder = models.TextField(null=True)
    headaches = models.TextField(null=True)
    head_injury = models.TextField(null=True)
    heart_condition = models.TextField(null=True)
    hepatitis = models.TextField(null=True)
    hernia = models.TextField(null=True)
    hyper_tension = models.TextField(null=True)
    hiv_aids = models.TextField(null=True)
    hospitalizations = models.TextField(null=True)
    ibd = models.TextField(null=True)
    kidney_urinary = models.TextField(null=True)
    medications = models.TextField(null=True)
    meningitis = models.TextField(null=True)
    mononucleosis = models.TextField(null=True)
    mrsa = models.TextField(null=True)
    organ_loss = models.TextField(null=True)
    pneumonia = models.TextField(null=True)
    rheumatic_fever = models.TextField(null=True)
    seizure_disorder = models.TextField(null=True)
    stroke = models.TextField(null=True)
    thyroid_disorder = models.TextField(null=True)
    tuberculosis = models.TextField(null=True)
    other_condition = models.TextField(null=True)
    # student mental health
    trouble_sleeping = models.TextField(null=True)
    more_energy = models.TextField(null=True)
    recurring_thoughts = models.TextField(null=True)
    anxious_nervious = models.TextField(null=True)
    depressed = models.TextField(null=True)
    lack_confidence = models.TextField(null=True)
    overwhelmed = models.TextField(null=True)
    lack_emotional_control = models.TextField(null=True)
    self_others_harm = models.TextField(null=True)
    lost_interest = models.TextField(null=True)
    isolated_alone = models.TextField(null=True)
    counseling = models.TextField(null=True)
    self_harm = models.TextField(null=True)
    # commented out the above after migration
    depression = models.TextField(null=True)
    anxiety = models.TextField(null=True)
    eating_disorder = models.TextField(null=True)
    adhd_add = models.TextField(null=True)
    substance_abuse = models.TextField(null=True)
    other_mental_health = models.TextField(null=True)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'student_medical_history'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current medical history academic year."""
        return self.created_at > day


class AthleteMedicalHistory(models.Model):
    """Athlete Medical History data model."""

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
    # athlete medical history
    exertional_syncope = models.TextField(null=True)
    heat_illness = models.TextField(null=True)
    intense_chest_pain = models.TextField(null=True)
    # Heart Health Questions about You and Your Family
    passed_out = models.TextField(null=True)
    chest_pain = models.TextField(null=True)
    skip_beats = models.TextField(null=True)
    high_cholesterol = models.TextField(null=True)
    kawasaki_disease = models.TextField(null=True)
    heart_infection = models.TextField(null=True)
    heart_test = models.TextField(null=True)
    lightheaded = models.TextField(null=True)
    unexplained_seizure = models.TextField(null=True)
    tired_quickly = models.TextField(null=True)
    sudden_death = models.TextField(null=True)
    sudden_cardiac_death = models.TextField(null=True)
    family_heart_problems = models.TextField(null=True)
    fainting_seizures = models.TextField(null=True)
    # Head and Neck Injury
    concussion = models.TextField(null=True)
    suspected_concussion = models.TextField(null=True)
    head_injuries = models.TextField(null=True)
    season_ending = models.TextField(null=True)
    cervical_injury = models.TextField(null=True)
    stinger_injury = models.TextField(null=True)
    neurologist_treatment = models.TextField(null=True)
    spine_injury = models.TextField(null=True)
    history_headaches = models.TextField(null=True)
    history_migraines = models.TextField(null=True)
    abdomen_injury = models.TextField(null=True)
    rib_injury = models.TextField(null=True)
    lumbar_injury = models.TextField(null=True)
    # Upper Extremity Injury
    shoulder_fracture = models.TextField(null=True)
    shoulder_dislocation = models.TextField(null=True)
    shoulder_muscle = models.TextField(null=True)
    labrum_injury = models.TextField(null=True)
    forearm_injury = models.TextField(null=True)
    elbow_injury = models.TextField(null=True)
    wrist_injury = models.TextField(null=True)
    finger_injury = models.TextField(null=True)
    # Lower Extremity Injury
    hip_pelvis = models.TextField(null=True)
    hamstring = models.TextField(null=True)
    quadriceps = models.TextField(null=True)
    thigh_other = models.TextField(null=True)
    knee_ligaments = models.TextField(null=True)
    meniscus = models.TextField(null=True)
    patella = models.TextField(null=True)
    knee_other = models.TextField(null=True)
    shin_splints = models.TextField(null=True)
    stress_fractures = models.TextField(null=True)
    compartment_syndrome = models.TextField(null=True)
    lower_leg_other = models.TextField(null=True)
    ankle_fracture = models.TextField(null=True)
    ankle_sprain = models.TextField(null=True)
    foot = models.TextField(null=True)
    toe = models.TextField(null=True)
    # Ears, Eyes, Dental
    glasses = models.TextField(null=True)
    contact_lenses = models.TextField(null=True)
    hearing_aids = models.TextField(null=True)
    dental_appliances = models.TextField(null=True)
    previous_year_change = models.TextField(null=True)
    physician_prohibition = models.TextField(null=True)
    # student mental health
    trouble_sleeping = models.TextField(null=True)
    more_energy = models.TextField(null=True)
    recurring_thoughts = models.TextField(null=True)
    anxious_nervious = models.TextField(null=True)
    depressed = models.TextField(null=True)
    lack_confidence = models.TextField(null=True)
    despair = models.TextField(null=True)
    lack_emotional_control = models.TextField(null=True)
    self_others_harm = models.TextField(null=True)
    mental_health_check = models.TextField(null=True, blank=True)
    # misc
    other_information = models.TextField(null=True)
    supplements = models.TextField(null=True)
    # Female Athletes Only
    menstrual_cycle = models.TextField(null=True)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'athlete_medical_history'

    def __str__(self):
        """Default data for display."""
        return self.user.username

    def current(self, day):
        """Determine if this is the current medical history academic year."""
        return self.created_at > day


@receiver(models.signals.post_save, sender=AthleteMedicalHistory)
def harm_email(sender, instance, **kwargs):
    """send an email if student indicates an inclination to harm self/others."""
    if not settings.ACADEMIC_YEAR_LIMBO:
        user = instance.user
        if instance.self_others_harm and instance.self_others_harm != 'No':
            to_list = settings.HARM_EMAIL_LIST
            if settings.DEBUG:
                to_list = [settings.SERVER_EMAIL]
            send_mail(
                None,
                to_list,
                '[Harm Self or Others] {0}, {1} ({2})'.format(
                    user.last_name,
                    user.first_name,
                    user.id,
                ),
                user.email,
                'medical_history/harm_email.html',
                instance,
                [settings.MANAGERS[0][1]],
            )
        if instance.mental_health_check == 'Yes':
            to_list = settings.MENTAL_HEALTH_CHECK
            if settings.DEBUG:
                to_list = [settings.SERVER_EMAIL]
            send_mail(
                None,
                to_list,
                '[Mental Health Check] {0}, {1} ({2})'.format(
                    user.last_name,
                    user.first_name,
                    user.id,
                ),
                user.email,
                'medical_history/mental_health_check.html',
                instance,
                [settings.MANAGERS[0][1]],
            )
