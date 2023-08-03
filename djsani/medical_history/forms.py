# -*- coding: utf-8 -*-

"""Forms for medical history."""

from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator
from djtools.fields import BINARY_CHOICES
from djtools.fields import REQ_CSS


ALLOWED_IMAGE_EXTENSIONS = settings.ALLOWED_IMAGE_EXTENSIONS
MENTAL_HEALTH_CHECK = (
    ('Yes', 'Yes'),
    (
        'No',
        'No, I feel confident that I can contact help if needed.',
    ),
)


class StudentMedicalHistoryForm(forms.Form):
    """Medical history for all students."""

    covid19_positive_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    covid19_positive = forms.CharField(
        label="Have you tested positive for COVID-19?",
        help_text="""
            If yes, please provide the month and year in your explanation
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    covid19_vacination_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    covid19_vacination = forms.CharField(
        label="Have received the COVID-19 vaccination?",
        help_text="""
            If yes, please provide the month and year in your explanation
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    allergies_medical_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    allergies_medical = forms.CharField(
        label="Do you have any allergies to medicine?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    allergies_other_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    allergies_other = forms.CharField(
        label="Do you have any seasonal, environmental, or food allergies?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    medications_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    medications = forms.CharField(
        label="Do you take any medications on a routine basis?",
        help_text="""
            This should include prescription & over the counter medicines
            (name, dose, frequency).
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    hospitalizations_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hospitalizations = forms.CharField(
        label="Have you had any hospitalizations or surgeries?",
        help_text="""
            If yes, please provide the year(s) in your explanation.
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    chicken_pox_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    chicken_pox = forms.CharField(
        label="Have you had chicken pox?",
        help_text="""
            If yes, please provide the month and year in your explanation.
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    organ_loss_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    organ_loss = forms.CharField(
        label="Absence/Loss of organ",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    substance_abuse_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    substance_abuse = forms.CharField(
        label="Alcohol/Substance abuse",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    anemia_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    anemia = forms.CharField(
        label="Anemia/Iron deficiency",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    bronchospasm_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    bronchospasm = forms.CharField(
        label="Asthma/Exertion induced bronchospasm",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    birth_defect_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    birth_defect = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    blood_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    blood_disorder = forms.CharField(
        label="Bleeding/Blood disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    bronchitis_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    bronchitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
        label="Bronchitis (recurrent)",
    )
    cancer_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    cancer = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    diabetes_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    diabetes = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    ent_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    ent_disorder = forms.CharField(
        label="Ear, nose, and throat disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    headaches_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    headaches = forms.CharField(
        label="Headaches (recurrent)",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    head_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    head_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    heart_condition_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    heart_condition = forms.CharField(
        label="Heart condition/murmur",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    hepatitis_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hepatitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    hernia_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hernia = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    hyper_tension_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hyper_tension = forms.CharField(
        label="High blood pressure",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    hiv_aids_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hiv_aids = forms.CharField(
        label="HIV/AIDS",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    mononucleosis_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    mononucleosis = forms.CharField(
        label="Infectious mononucleosis",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    ibd_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    ibd = forms.CharField(
        label="Inflammatory bowel disease",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    kidney_urinary_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    kidney_urinary = forms.CharField(
        label="Kidney/Urinary tract problems",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    meningitis_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    meningitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    mrsa_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    mrsa = forms.CharField(
        label="MRSA/Staph infection",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    pneumonia_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    pneumonia = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    rheumatic_fever_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    rheumatic_fever = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    seizure_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    seizure_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    stroke_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    stroke = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    thyroid_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    thyroid_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    tuberculosis_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    tuberculosis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    other_condition_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    other_condition = forms.CharField(
        label="""
            Do you have any illness or medical condition not listed above
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    depression_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    depression = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    anxiety_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    anxiety = forms.CharField(
        label="Anxiety/Panic attacks",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    eating_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    eating_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    adhd_add_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    adhd_add = forms.CharField(
        label="""
            Attention Deficit Hyperactivity Disorder
            / Attention Deficit Disorder (ADHD/ADD)
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    substance_abuse_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    substance_abuse = forms.CharField(
        label="Alcohol/Substance Abuse Disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    other_mental_health_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    other_mental_health = forms.CharField(
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )

    def __init__(self, *args, **kwargs):
        """Initialisation of the form that accepts a 'gender' value."""
        kwargs.pop('gender', 0)
        super(StudentMedicalHistoryForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Form validation."""
        cd = self.cleaned_data
        for field, _ in cd.items():
            if cd[field] == 'Yes' and not cd.get('{0}_2'.format(field)):
                self._errors[field] = self.error_class([
                    """
                        Explain your 'Yes' response or type 'No'
                        to respond in the negative.
                    """,
                ])
        return self.cleaned_data


class AthleteMedicalHistoryForm(forms.Form):
    """Medical history for student athletes."""

    exertional_syncope_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    exertional_syncope = forms.CharField(
        help_text="(fainting during exercise)",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    heat_illness_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    heat_illness = forms.CharField(
        help_text="History of heat illness?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    intense_chest_pain_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    intense_chest_pain = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Heart Health Questions about You and Your Family
    passed_out_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    passed_out = forms.CharField(
        label="""
            Have you ever passed out or nearly passed out
            DURING or AFTER exercise?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    chest_pain_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    chest_pain = forms.CharField(
        label="""
            Have you ever had discomfort, pain, tightness, or pressure
            in your chest during exercise?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    skip_beats_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    skip_beats = forms.CharField(
        label="""
            Does your heart ever race or skip beats (irregular beats)
            during exercise?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    high_cholesterol_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    high_cholesterol = forms.CharField(
        label="""
            Has a doctor ever told you that you have high cholesterol?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    kawaski_disease_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    kawasaki_disease = forms.CharField(
        label="""
            Has a doctor ever told you that you have Kawasaki disease?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    heart_infection_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    heart_infection = forms.CharField(
        label="""
            Has a doctor ever told you that you have or had a heart infection?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    heart_test_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    heart_test = forms.CharField(
        label="""
            Has doctor ever ordered a test for your heart
            (For example, ECG/EKG, echocardiogram)?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    lightheaded_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    lightheaded = forms.CharField(
        label="""
            Do you get lightheaded or feel more short of breath than expected
            during exercise?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    unexplained_seizure_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    unexplained_seizure = forms.CharField(
        label="""
            Have you ever had an unexplained seizure?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    tired_quickly_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    tired_quickly = forms.CharField(
        label="""
            Do you get more tired or short of breath more quickly
            than your friends during exercise?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    sudden_death_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    sudden_death = forms.CharField(
        label="""
            Has any family member or relative died of heart problems
            or had an unexpected or unexplained sudden death before age 50
            (including drowning, unexplained car accident, or
            sudden infant death syndrome)?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    sudden_cardiac_death_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    sudden_cardiac_death = forms.CharField(
        label="""
            Does anyone in your family have hypertrophic cardiomyopathy,
            Marfan syndrome, arrhythmogenic right ventricular cardiomyopathy,
            long QT syndrome, short QT syndrome, Brugada syndrome, or
            catecholaminergic polymorphic ventricular tachycardia?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    family_heart_problems_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    family_heart_problems = forms.CharField(
        label="""
            Does anyone in your family have a heart problem, pacemaker,
            or implanted defibrillator?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    fainting_seizures_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    fainting_seizures = forms.CharField(
        label="""
            Has anyone in your family had unexplained fainting,
            unexplained seizures, or near drowning?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Head and Neck Injury
    head_injuries_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    head_injuries = forms.CharField(
        label='Multiple head injuries',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    concussion_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    concussion = forms.CharField(
        label='Diagnosed concussion (#)',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    suspected_concussion_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    suspected_concussion = forms.CharField(
        label='Suspected, unreported concussion (#)',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    season_ending_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    season_ending = forms.CharField(
        label="Season ending head injuries",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    cervical_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    cervical_injury = forms.CharField(
        label="Cervical (neck) injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    stinger_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    stinger_injury = forms.CharField(
        label='"Stinger" or "Burner" injury',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    neurologist_treatment_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    neurologist_treatment = forms.CharField(
        label="Injury requiring neurologist treatment",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    spine_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    spine_injury = forms.CharField(
        label="Spine or vertebral disc injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    history_headaches_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    history_headaches = forms.CharField(
        label="History of headaches",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    history_migraines_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    history_migraines = forms.CharField(
        label="History of migraine headaches",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # *** Torso Injury
    abdomen_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    abdomen_injury = forms.CharField(
        label="Abdomen/Thoracic injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    rib_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    rib_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    lumbar_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    lumbar_injury = forms.CharField(
        label="Lumbar/Sacral injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Upper Extremity Injury
    #
    # Shoulder/Clavicle
    shoulder_fracture_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    shoulder_fracture = forms.CharField(
        label="Fracture",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    shoulder_dislocation_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    shoulder_dislocation = forms.CharField(
        label="Dislocation/Subluxation",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    shoulder_muscle_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    shoulder_muscle = forms.CharField(
        label="Muscle injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    labrum_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    labrum_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    forearm_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    forearm_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    elbow_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    elbow_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    wrist_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    wrist_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    finger_injury_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    finger_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Lower Extremity Injury
    hip_pelvis_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hip_pelvis = forms.CharField(
        label="Hip/Pelvis",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # *** Thigh
    hamstring_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hamstring = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    quadriceps_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    quadriceps = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    thigh_other_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    thigh_other = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # *** Knee
    knee_ligaments_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    knee_ligaments = forms.CharField(
        label="Ligaments",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    meniscus_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    meniscus = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    patella_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    patella = forms.CharField(
        help_text='',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    knee_other_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    knee_other = forms.CharField(
        label="Other",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # *** Lower leg
    shin_splints_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    shin_splints = forms.CharField(
        label="MTSS/Shin splints",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    stress_fractures_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    stress_fractures = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    compartment_syndrome_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    compartment_syndrome = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    lower_leg_other_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    lower_leg_other = forms.CharField(
        label="Other",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # *** Ankle
    ankle_fracture_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    ankle_fracture = forms.CharField(
        label="Fracture",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    ankle_sprain_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    ankle_sprain = forms.CharField(
        label="Sprain/Strain",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # foot and toe
    foot_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    foot = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    toe_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    toe = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Ears, Eyes, Dental
    glasses_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    glasses = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    contact_lenses_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    contact_lenses = forms.CharField(
        help_text="If yes, indicate hard or soft lenses",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    hearing_aids_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    hearing_aids = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    dental_appliances_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    dental_appliances = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Additional Medical Information
    physician_prohibition_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    physician_prohibition = forms.CharField(
        label="""
            Has a physician ever limited/restricted you
            from athletic participation?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # mental health
    trouble_sleeping_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    trouble_sleeping = forms.CharField(
        label="I often have trouble sleeping.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    more_energy_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    more_energy = forms.CharField(
        label="I wish I had more energy most days of the week.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    recurring_thoughts_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    recurring_thoughts = forms.CharField(
        label="I think about things over and over.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    anxious_nervious_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    anxious_nervious = forms.CharField(
        label="I feel anxious and nervous much of the time.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    depressed_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    depressed = forms.CharField(
        label="I often feel sad or depressed.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    lack_confidence_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    lack_confidence = forms.CharField(
        label="I struggle with being confident.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    despair_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    despair = forms.CharField(
        label="I don’t feel hopeful about the future.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    lack_emotional_control_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    lack_emotional_control = forms.CharField(
        label="""
            I have a hard time managing my emotions (frustration, anger,
            impatience).
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    self_others_harm_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    self_others_harm = forms.CharField(
        label="I have feelings of hurting myself or others.",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    mental_health_check = forms.CharField(
        label="Would you like someone from health and counseling to reach out to you?",
        max_length=255,
        required=False,
        widget=forms.RadioSelect(choices=MENTAL_HEALTH_CHECK, attrs=REQ_CSS),
    )
    # misc
    other_information_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    other_information = forms.CharField(
        label="""
            Any other health or medical related information
            not covered above?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    supplements_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    supplements = forms.CharField(
        label="""
            Are you taking any ergogenic aids/vitamin supplements?
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
    )
    # Female Athletes Only
    menstrual_cycle_2 = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    menstrual_cycle = forms.CharField(
        label="Do you have an irregular menstrual cycle?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ_CSS),
        initial="No",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """Initialisation of the form that accepts a 'gender' value."""
        gender = kwargs.pop('gender', 0)
        super(AthleteMedicalHistoryForm, self).__init__(*args, **kwargs)
        if gender == 'M':
            self.fields.pop('menstrual_cycle')
            self.fields.pop('menstrual_cycle_2')

    def clean(self):
        """Form validation."""
        cd = self.cleaned_data
        for field, _ in cd.items():
            if field != 'mental_health_check':
                if cd[field] == 'Yes' and not cd.get('{0}_2'.format(field)):
                    self._errors[field] = self.error_class(
                        ["Explain your 'Yes' response"],
                    )
            else:
                if cd.get('self_others_harm') == 'Yes' and not cd.get('mental_health_check'):
                    self._errors['mental_health_check'] = self.error_class(
                        ['Please choose "Yes" or "No"'],
                    )

        return self.cleaned_data


class PhysicalEvaluationForm(forms.Form):
    """Medical Physical evaluation form."""

    physical_evaluation_1 = forms.FileField(
        label="Upload page 1 of the form",
        help_text="""
            Photo or scan of your physical evaluation form signed by your doctor
        """,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS),
        ],
        required=True,
    )
    physical_evaluation_2 = forms.FileField(
        label="Upload page 2 of the form",
        help_text="""
            Photo or scan of your physical evaluation form signed by your doctor
        """,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS),
        ],
        required=True,
    )


class MedicalConsentAgreementForm(forms.Form):
    """Medical consent agreement form class."""

    medical_consent_agreement = forms.FileField(
        label="Upload your file",
        help_text="""
            Photo or scan of your signed medical consent and
            medical insurance agreement form
        """,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS),
        ],
        required=True,
    )


class Covid19VaccineCardForm(forms.Form):
    """COVID-19 Vaccine Card form class."""

    covid19_vaccine_card = forms.FileField(
        label="Upload your file",
        help_text="Photo or scan of your COVID-19 vaccine card.",
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS),
        ],
        required=True,
    )
