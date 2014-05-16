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
    allergies_medical = forms.CharField(
        label = "Do you have any allergies to medicine?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    allergies_other = forms.CharField(
        label = "Do you have any seasonal, environmental, or food allergies?",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    medications = forms.CharField(
        label = "Do you take any medications on a routine basis?",
        help_text = """
            This should include prescription & over the counter medicines
            (name, dose, frequency)
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hospitalizations = forms.CharField(
        label = "Have you had any hospitalizations or surgeries?",
        help_text = """
            If yes, please provide the year(s) in your explanation
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    chicken_pox = forms.CharField(
        label = "Have you had chicken pox?",
        help_text = """
            If yes, please provide the month and year in your explanation
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    organ_loss = forms.CharField(
        label = "Absence/Loss of organ",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    substance_abuse = forms.CharField(
        label = "Alcohol/Substance abuse",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    anemia = forms.CharField(
        label = "Anemia/Iron deficiency",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    anxiety = forms.CharField(
        label = "Anxiety/Panic attacks",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    bronchospasm = forms.CharField(
        label = "Asthma/Exertion induced bronchospasm",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    adhd_add = forms.CharField(
        label = """
                Attention Deficit Hyperactivity Disorder
                / Attention Deficit Disorder (ADHD/ADD)
                """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    birth_defect = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    blood_disorder = forms.CharField(
        label = "Bleeding/Blood disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    bronchitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        label = "Bronchitis (recurrent)",
        required=False
    )
    cancer = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    counseling = forms.CharField(
        label = "Counseling/Mental health treatment",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    depression = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    diabetes = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    eating_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    ent_disorder = forms.CharField(
        label = "Ear, nose, and throat disorder",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    headaches = forms.CharField(
        label = "Headaches (recurrent)",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    head_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    heart_condition = forms.CharField(
        label = "Heart condition/murmur",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hepatitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hernia = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hyper_tension = forms.CharField(
        label = "High blood pressure",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hiv_aids = forms.CharField(
        label = "HIV/AIDS",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    mononucleosis = forms.CharField(
        label = "Infectious mononucleosis",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    ibd = forms.CharField(
        label = "Inflammatory bowel disease",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    kidney_urinary = forms.CharField(
        label = "Kidney/Urinary tract problems",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    meningitis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    mrsa = forms.CharField(
        label = "MRSA/Staph infection",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    pneumonia = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    rheumatic_fever = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    seizure_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    stroke = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    thyroid_disorder = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    tuberculosis = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    other_condition = forms.CharField(
        label = """
            Do you have any illness or medical condition not listed above
        """,
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(StudentForm,self).__init__(*args,**kwargs)
        #self.fields.keyOrder = []

class AthleteForm(forms.Form):
    """
    Medical history for student athletes
    """
    exertional_syncope = forms.CharField(
        help_text="(fainting during exercise)",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    heat_illness = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    intense_chest_pain = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    sickle_cell_trait = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Head and Neck Injury
    concussion = forms.CharField(
        label='Diagnosed concussion (#)',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    suspected_concussion = forms.CharField(
        label='Suspected, unreported concussion (#)',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    head_injuries = forms.CharField(
        label='Multiple head injuries',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    season_ending = forms.CharField(
        label="Season ending head injuries",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    cervical_injury = forms.CharField(
        label="Cervical (neck) injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    stinger_injury      = forms.CharField(
        label='"Stinger" or "Burner" injury',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    neurologist_treatment = forms.CharField(
        label="Injury requiring neurologist treatment",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    spine_injury = forms.CharField(
        label="Spine or vertebral disc injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    history_headaches = forms.CharField(
        label="History of headaches",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    history_migraines = forms.CharField(
        label="History of migraine headaches",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Torso Injury
    abdomen_injury = forms.CharField(
        label="Abdomen/Thoracic injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    rib_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
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
    shoulder_fracture = forms.CharField(
        label="Fracture",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    shoulder_dislocation = forms.CharField(
        label="Dislocation/Subluxation",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    shoulder_muscle = forms.CharField(
        label="Muscle injury",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    labrum_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    forearm_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    elbow_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    wrist_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    finger_injury = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Lower Extremity Injury
    hip_pelvis = forms.CharField(
        label="Hip/Pelvis",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Thigh
    hamstring = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    quadriceps = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    thigh_other = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Knee
    knee_ligaments= forms.CharField(
        label="Ligaments",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    meniscus = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    patella = forms.CharField(
        help_text='',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    knee_other = forms.CharField(
        label="Other",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Lower leg
    shin_splints = forms.CharField(
        label="MTSS/Shin splints",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    stress_fractures = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    compartment_syndrome = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    lower_leg_other = forms.CharField(
        label="Other",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    #### Ankle
    ankle_fracture = forms.CharField(
        label="Fracture",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    ankle_sprain = forms.CharField(
        label="Sprain/Strain",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # foot and toe
    foot = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    toe = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Ears, Eyes, Dental
    glasses = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    contact_lenses = forms.CharField(
        help_text='If yes, indicate hard or soft lenses',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    hearing_aids = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    dental_appliances = forms.CharField(
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
    )
    # Additional Medical Information
    previous_year_change = forms.CharField(
        label='''
            Any change in current medications or allergies
            from previous year?
        ''',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
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
    other_information = forms.CharField(
        label='''
            Any other health or medical related information
            not covered above?
        ''',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        required=False
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
    menstrual_cycle = forms.CharField(
        label="Do you have an irregular menstrual cycle?",
        #help_text='Males, select "No".',
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ_CSS),
        initial="No",
        required=False
    )

