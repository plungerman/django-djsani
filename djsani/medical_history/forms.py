# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

#from djtools.fields import BINARY_CHOICES
from djzbar.utils.informix import do_sql

BINARY_CHOICES = (
    ('No', 'No'),
    ('Yes', 'Yes'),
)

class AcademicsForm(forms.Form):
    """
     = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    """
    allergies_medical = forms.CharField(
        label = "Medical allergies",
        max_length=255,
        widget=forms.RadioSelect(choices=BINARY_CHOICES),
        required=False
    )
    allergies_other = forms.ChoiceField(
        label = "Seasonal, environmental, or food allergies",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    anemia = forms.ChoiceField(
        label = "Anemia/Iron deficiency",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    anxiety = forms.ChoiceField(
        label = "Anxiety/Panic attacks",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    bronchospasm = forms.ChoiceField(
        label = "Asthma/Exertion induced bronchospasm",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    adhd_add = forms.ChoiceField(
        label = """
                Attention Deficit Hyperactivity Disorder
                / Attention Deficit Disorder (ADHD/ADD)
                """,
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    birth_defect = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    blood_disorder = forms.ChoiceField(
        label = "Bleeding/Blood disorder",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    bronchitis = forms.ChoiceField(
        label = "Bronchitis (recurrent)",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    cancer = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    chicken_pox = forms.ChoiceField(
        label = "Have you had chicken pox?",
        help_text = """
            If yes, please provide the month and year in your explanation
        """,
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    counseling = forms.ChoiceField(
        label = "Counseling/Mental health treatment",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    depression = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    diabetes = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    eating_disorder = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    ent_disorder = forms.ChoiceField(
        label = "Ear, Nose and Throat disorder",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    headaches = forms.ChoiceField(
        label = "Headaches (recurrent)",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    head_injury = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    heart_condition = forms.ChoiceField(
        label = "Heart Condition/Murmur",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    hepatitis = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    hernia = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    hyper_tension = forms.ChoiceField(
        label = "High blood pressure",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    hiv_aids = forms.ChoiceField(
        label = "HIV/AIDS",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    hospitalizations = forms.ChoiceField(
        label = "Hospitalizations & surgeries",
        help_text = """
            If yes, please provide the year(s) in your explanation
        """,
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    ibd = forms.ChoiceField(
        label = "Inflammatory Bowel Disease",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    kidney_urinary = forms.ChoiceField(
        label = "Kidney/Urinary tract problems",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    medications = forms.ChoiceField(
        label = "Routine medications",
        help_text = """
            Prescription & over the counter medicines
            (name, dose, frequency)
        """,
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    meningitis = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    mononucleosis = forms.ChoiceField(
        label = "Infectious mononucleosis",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    mrsa = forms.ChoiceField(
        label = "MRSA/Staph infection",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    organ_loss = forms.ChoiceField(
        label = "Absence/Loss of organ",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    pneumonia = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    rheumatic_fever = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    seizure_disorder = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    stroke = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    substance_abuse = forms.ChoiceField(
        label = "Alcohol/Substance abuse",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    thyroid_disorder = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    tuberculosis = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    other_condition = forms.ChoiceField(
        label = "Illness or medical condition not listed above",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )

    def __init__(self,*args,**kwargs):
        super(AcademicsForm,self).__init__(*args,**kwargs)
        #self.fields.keyOrder = []

class AthleticsForm(forms.Form):
    """
     = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    """
    def __init__(self,*args,**kwargs):
        super(AthleticsForm,self).__init__(*args,**kwargs)
        #self.fields.keyOrder = []

def _put_data(forms,status=0):
    # we pass 'status' to this method which is the
    # len() of the data set returned from informix
    # via the _get_data() method.
    if status==1:
        prefix = "update student_medical_history"
    else:
        prefix = "insert into student_medical_history"
    sql = "%s " % prefix
    if not settings.DEBUG:
        do_sql(sql, key=settings.INFORMIX_DEBUG)

def _get_data(cid,fname):
    data = {}
    # dictionary to populate form on GET
    data["form"] = {}
    if not settings.DEBUG:
        sql = "select * from in student_medical_history where cid = '%s'" % cid
        results = do_sql(sql, key=settings.INFORMIX_DEBUG)
        obj = results.fetchall()
        # if len() == 0, insert; if len() == 1, update
        data["status"] = len(obj)
        if data["status"] == 1:
            form = eval(fname)()
            for f in form.field:
                data["form"][f] = obj["%s"] % f
    else:
        data["status"] = 0
    return data
