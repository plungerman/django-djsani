# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from djtools.fields import REQ_CSS

BINARY_CHOICES = (
    ('No', 'No'),
    ('Yes', 'Yes'),
)

class StudentForm(forms.Form):
    """
    Medical history for all students
    """
    allergies_medical_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    allergies_medical = forms.CharField(
        label = "Do you have any allergies to medicine?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    allergies_other_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    allergies_other = forms.CharField(
        label = "Do you have any seasonal, environmental, or food allergies?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    medications_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    medications = forms.CharField(
        label = "Do you take any medications on a routine basis?",
        help_text = """
            This should include prescription & over the counter medicines
            (name, dose, frequency)
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    hospitalizations_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hospitalizations = forms.CharField(
        label = "Have you had any hospitalizations or surgeries?",
        help_text = """
            If yes, please provide the year(s) in your explanation
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    chicken_pox_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    chicken_pox = forms.CharField(
        label = "Have you had chicken pox?",
        help_text = """
            If yes, please provide the month and year in your explanation
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    organ_loss_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    organ_loss = forms.CharField(
        label = "Absence/Loss of organ",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    substance_abuse_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    substance_abuse = forms.CharField(
        label = "Alcohol/Substance abuse",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    anemia_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    anemia = forms.CharField(
        label = "Anemia/Iron deficiency",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    anxiety_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    anxiety = forms.CharField(
        label = "Anxiety/Panic attacks",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    bronchospasm_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    bronchospasm = forms.CharField(
        label = "Asthma/Exertion induced bronchospasm",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    adhd_add_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    adhd_add = forms.CharField(
        label = """
                Attention Deficit Hyperactivity Disorder
                / Attention Deficit Disorder (ADHD/ADD)
                """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    birth_defect_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    birth_defect = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    blood_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    blood_disorder = forms.CharField(
        label = "Bleeding/Blood disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    bronchitis_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    bronchitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        label = "Bronchitis (recurrent)",
    )
    cancer_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    cancer = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    counseling_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    counseling = forms.CharField(
        label = "Counseling/Mental health treatment",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    depression_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    depression = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    diabetes_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    diabetes = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    eating_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    eating_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    ent_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    ent_disorder = forms.CharField(
        label = "Ear, nose, and throat disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    headaches_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    headaches = forms.CharField(
        label = "Headaches (recurrent)",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    head_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    head_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    heart_condition_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    heart_condition = forms.CharField(
        label = "Heart condition/murmur",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    hepatitis_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hepatitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    hernia_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hernia = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    hyper_tension_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hyper_tension = forms.CharField(
        label = "High blood pressure",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    hiv_aids_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hiv_aids = forms.CharField(
        label = "HIV/AIDS",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    mononucleosis_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    mononucleosis = forms.CharField(
        label = "Infectious mononucleosis",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    ibd_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    ibd = forms.CharField(
        label = "Inflammatory bowel disease",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    kidney_urinary_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    kidney_urinary = forms.CharField(
        label = "Kidney/Urinary tract problems",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    meningitis_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    meningitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    mrsa_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    mrsa = forms.CharField(
        label = "MRSA/Staph infection",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    pneumonia_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    pneumonia = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    rheumatic_fever_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    rheumatic_fever = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    seizure_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    seizure_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    stroke_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    stroke = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    thyroid_disorder_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    thyroid_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    tuberculosis_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    tuberculosis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )
    other_condition_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    other_condition = forms.CharField(
        label = """
            Do you have any illness or medical condition not listed above
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
    )

    def clean(self):
        cd = self.cleaned_data
        for field in cd:
            if cd[field] == "Yes" and not cd.get("%s_2" % field):
                self._errors[field] = self.error_class(
                    ["Explain your 'Yes' response"]
                )
        return self.cleaned_data


class AthleteForm(forms.Form):
    """
    Medical history for student athletes
    """

    exertional_syncope_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    exertional_syncope = forms.CharField(
        help_text="(fainting during exercise)",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    heat_illness_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    heat_illness = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    intense_chest_pain_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    intense_chest_pain = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    sickle_cell_trait_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    sickle_cell_trait = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Head and Neck Injury
    concussion_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    concussion = forms.CharField(
        label='Diagnosed concussion (#)',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    suspected_concussion_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    suspected_concussion = forms.CharField(
        label='Suspected, unreported concussion (#)',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    head_injuries_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    head_injuries = forms.CharField(
        label='Multiple head injuries',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    season_ending_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    season_ending = forms.CharField(
        label="Season ending head injuries",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    cervical_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    cervical_injury = forms.CharField(
        label="Cervical (neck) injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    stinger_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    stinger_injury = forms.CharField(
        label='"Stinger" or "Burner" injury',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    neurologist_treatment_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    neurologist_treatment = forms.CharField(
        label="Injury requiring neurologist treatment",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    spine_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    spine_injury = forms.CharField(
        label="Spine or vertebral disc injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    history_headaches_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    history_headaches = forms.CharField(
        label="History of headaches",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    history_migraines_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    history_migraines = forms.CharField(
        label="History of migraine headaches",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Torso Injury
    abdomen_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    abdomen_injury = forms.CharField(
        label="Abdomen/Thoracic injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    rib_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    rib_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    lumbar_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    lumbar_injury = forms.CharField(
        label="Lumbar/Sacral injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Upper Extremity Injury
    #
    # Shoulder/Clavicle
    shoulder_fracture_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    shoulder_fracture = forms.CharField(
        label="Fracture",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    shoulder_dislocation_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    shoulder_dislocation = forms.CharField(
        label="Dislocation/Subluxation",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    shoulder_muscle_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    shoulder_muscle = forms.CharField(
        label="Muscle injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    labrum_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    labrum_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    forearm_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    forearm_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    elbow_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    elbow_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    wrist_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    wrist_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    finger_injury_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    finger_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Lower Extremity Injury
    hip_pelvis_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hip_pelvis = forms.CharField(
        label="Hip/Pelvis",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Thigh
    hamstring_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hamstring = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    quadriceps_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    quadriceps = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    thigh_other_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    thigh_other = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Knee
    knee_ligaments_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    knee_ligaments= forms.CharField(
        label="Ligaments",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    meniscus_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    meniscus = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    patella_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    patella = forms.CharField(
        help_text='',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    knee_other_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    knee_other = forms.CharField(
        label="Other",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Lower leg
    shin_splints_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    shin_splints = forms.CharField(
        label="MTSS/Shin splints",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    stress_fractures_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    stress_fractures = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    compartment_syndrome_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    compartment_syndrome = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    lower_leg_other_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    lower_leg_other = forms.CharField(
        label="Other",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Ankle
    ankle_fracture_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    ankle_fracture = forms.CharField(
        label="Fracture",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    ankle_sprain_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    ankle_sprain = forms.CharField(
        label="Sprain/Strain",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # foot and toe
    foot_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    foot = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    toe_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    toe = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Ears, Eyes, Dental
    glasses_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    glasses = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    contact_lenses_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    contact_lenses = forms.CharField(
        help_text='If yes, indicate hard or soft lenses',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hearing_aids_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    hearing_aids = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    dental_appliances_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    dental_appliances = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Additional Medical Information
    previous_year_change_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    previous_year_change = forms.CharField(
        label='''
            Any change in current medications or allergies
            from previous year?
        ''',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    physician_prohibition_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    physician_prohibition = forms.CharField(
        label='''
            Has a physician ever limited/restricted you
            from athletic participation?
        ''',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    other_information_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    other_information = forms.CharField(
        label='''
            Any other health or medical related information
            not covered above?
        ''',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    supplements_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    supplements = forms.CharField(
        label='''
            Are you taking any ergogenic aids/vitamin supplements?
        ''',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Female Athletes Only
    menstrual_cycle_2 = forms.CharField(
        widget=forms.HiddenInput(),required=False
    )
    menstrual_cycle = forms.CharField(
        label="Do you have an irregular menstrual cycle?",
        #help_text='Males, select "No".',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        initial="No",
        required=False
    )

    def clean(self):
        cd = self.cleaned_data
        for field in cd:
            if cd[field] == "Yes" and not cd.get("%s_2" % field):
                self._errors[field] = self.error_class(
                    ["Explain your 'Yes' response"]
                )
        return self.cleaned_data

