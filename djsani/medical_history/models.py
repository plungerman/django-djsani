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
    college_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(
        StudentMedicalManager, on_delete=models.CASCADE,
    )
    # medical history fields
    covid19_positive = models.CharField(max_length=255)
    covid19_vacination = models.CharField(max_length=255)
    allergies_medical = models.CharField(max_length=255)
    allergies_other = models.CharField(max_length=255)
    anemia = models.CharField(max_length=255)
    bronchospasm = models.CharField(max_length=255)
    birth_defect = models.CharField(max_length=255)
    blood_disorder = models.CharField(max_length=255)
    bronchitis = models.CharField(max_length=255)
    cancer = models.CharField(max_length=255)
    chicken_pox = models.CharField(max_length=255)
    diabetes = models.CharField(max_length=255)
    ent_disorder = models.CharField(max_length=255)
    headaches = models.CharField(max_length=255)
    head_injury = models.CharField(max_length=255)
    heart_condition = models.CharField(max_length=255)
    hepatitis = models.CharField(max_length=255)
    hernia = models.CharField(max_length=255)
    hyper_tension = models.CharField(max_length=255)
    hiv_aids = models.CharField(max_length=255)
    hospitalizations = models.CharField(max_length=255)
    ibd = models.CharField(max_length=255)
    kidney_urinary = models.CharField(max_length=255)
    medications = models.CharField(max_length=255)
    meningitis = models.CharField(max_length=255)
    mononucleosis = models.CharField(max_length=255)
    mrsa = models.CharField(max_length=255)
    organ_loss = models.CharField(max_length=255)
    pneumonia = models.CharField(max_length=255)
    rheumatic_fever = models.CharField(max_length=255)
    seizure_disorder = models.CharField(max_length=255)
    stroke = models.CharField(max_length=255)
    thyroid_disorder = models.CharField(max_length=255)
    tuberculosis = models.CharField(max_length=255)
    other_condition = models.CharField(max_length=255)
    # student mental health
    # trouble_sleeping = models.CharField(max_length=255)
    # more_energy = models.CharField(max_length=255)
    # recurring_thoughts = models.CharField(max_length=255)
    # anxious_nervious = models.CharField(max_length=255)
    # depressed = models.CharField(max_length=255)
    # lack_confidence = models.CharField(max_length=255)
    # overwhelmed = models.CharField(max_length=255)
    # lack_emotional_control = models.CharField(max_length=255)
    # self_others_harm = models.CharField(max_length=255)
    # lost_interest = models.CharField(max_length=255)
    # isolated_alone = models.CharField(max_length=255)
    # counseling = models.CharField(max_length=255)
    depression = models.CharField(max_length=255)
    anxiety = models.CharField(max_length=255)
    eating_disorder = models.CharField(max_length=255)
    adhd_add = models.CharField(max_length=255)
    substance_abuse = models.CharField(max_length=255)
    # self_harm = models.CharField(max_length=255)
    other_mental_health = models.CharField(max_length=255)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_student_medical_history'

    def __repr__(self):
        """Default data for display."""
        return str(self.college_id)

    def current(self, day):
        """Determine if this is the current medical history academic year."""
        return self.created_at > day


class AthleteMedicalHistory(models.Model):
    """Athlete Medical History data model."""

    # core
    college_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(
        StudentMedicalManager, on_delete=models.CASCADE,
    )
    # athlete medical history
    exertional_syncope = models.CharField(max_length=255)
    heat_illness = models.CharField(max_length=255)
    intense_chest_pain = models.CharField(max_length=255)
    # Heart Health Questions about You and Your Family
    passed_out = models.CharField(max_length=255)
    chest_pain = models.CharField(max_length=255)
    skip_beats = models.CharField(max_length=255)
    high_cholesterol = models.CharField(max_length=255)
    kawasaki_disease = models.CharField(max_length=255)
    heart_infection = models.CharField(max_length=255)
    heart_test = models.CharField(max_length=255)
    lightheaded = models.CharField(max_length=255)
    unexplained_seizure = models.CharField(max_length=255)
    tired_quickly = models.CharField(max_length=255)
    sudden_death = models.CharField(max_length=255)
    sudden_cardiac_death = models.CharField(max_length=255)
    family_heart_problems = models.CharField(max_length=255)
    fainting_seizures = models.CharField(max_length=255)
    # Head and Neck Injury
    concussion = models.CharField(max_length=255)
    suspected_concussion = models.CharField(max_length=255)
    head_injuries = models.CharField(max_length=255)
    season_ending = models.CharField(max_length=255)
    cervical_injury = models.CharField(max_length=255)
    stinger_injury = models.CharField(max_length=255)
    neurologist_treatment = models.CharField(max_length=255)
    spine_injury = models.CharField(max_length=255)
    history_headaches = models.CharField(max_length=255)
    history_migraines = models.CharField(max_length=255)
    abdomen_injury = models.CharField(max_length=255)
    rib_injury = models.CharField(max_length=255)
    lumbar_injury = models.CharField(max_length=255)
    # Upper Extremity Injury
    shoulder_fracture = models.CharField(max_length=255)
    shoulder_dislocation = models.CharField(max_length=255)
    shoulder_muscle = models.CharField(max_length=255)
    labrum_injury = models.CharField(max_length=255)
    forearm_injury = models.CharField(max_length=255)
    elbow_injury = models.CharField(max_length=255)
    wrist_injury = models.CharField(max_length=255)
    finger_injury = models.CharField(max_length=255)
    # Lower Extremity Injury
    hip_pelvis = models.CharField(max_length=255)
    hamstring = models.CharField(max_length=255)
    quadriceps = models.CharField(max_length=255)
    thigh_other = models.CharField(max_length=255)
    knee_ligaments = models.CharField(max_length=255)
    meniscus = models.CharField(max_length=255)
    patella = models.CharField(max_length=255)
    knee_other = models.CharField(max_length=255)
    shin_splints = models.CharField(max_length=255)
    stress_fractures = models.CharField(max_length=255)
    compartment_syndrome = models.CharField(max_length=255)
    lower_leg_other = models.CharField(max_length=255)
    ankle_fracture = models.CharField(max_length=255)
    ankle_sprain = models.CharField(max_length=255)
    foot = models.CharField(max_length=255)
    toe = models.CharField(max_length=255)
    # Ears, Eyes, Dental
    glasses = models.CharField(max_length=255)
    contact_lenses = models.CharField(max_length=255)
    hearing_aids = models.CharField(max_length=255)
    dental_appliances = models.CharField(max_length=255)
    previous_year_change = models.CharField(max_length=255)
    physician_prohibition = models.CharField(max_length=255)
    # student mental health
    trouble_sleeping = models.CharField(max_length=255)
    more_energy = models.CharField(max_length=255)
    recurring_thoughts = models.CharField(max_length=255)
    anxious_nervious = models.CharField(max_length=255)
    depressed = models.CharField(max_length=255)
    lack_confidence = models.CharField(max_length=255)
    despair = models.CharField(max_length=255)
    lack_emotional_control = models.CharField(max_length=255)
    self_others_harm = models.CharField(max_length=255)
    # misc
    other_information = models.CharField(max_length=255)
    supplements = models.CharField(max_length=255)
    # Female Athletes Only
    menstrual_cycle = models.CharField(max_length=255)

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_athlete_medical_history'

    def __repr__(self):
        """Default data for display."""
        return str(self.college_id)

    def current(self, day):
        """Determine if this is the current medical history academic year."""
        return self.created_at > day


@receiver(models.signals.post_save, sender=AthleteMedicalHistory)
def harm_email(sender, instance, **kwargs):
    """send an email if student indicates an inclination to harm self/others."""
    if instance.self_others_harm and instance.self_others_harm != 'No':
        user = User.objects.get(pk=instance.college_id)
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
