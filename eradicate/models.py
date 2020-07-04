from django.db import models
from django import forms
from multiselectfield import MultiSelectField


class PatientBasicInfo(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_id = models.EmailField(max_length=100)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=False)
    age = models.PositiveIntegerField(default=False, null=True, blank=False)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    # bmi = models.FloatField(null=True)

    ETHNICITY_CHOICES = (
        ('indian', 'INDIAN'),
        ('asian', 'ASIAN'),
        ('american', 'AMERICAN'),
        ('latin', 'LATIN'),
        ('european', 'EUROPEAN'),
        ('australian', 'AUSTRALIAN'),
        ('others', 'OTHERS'),
    )

    ethnicity = models.CharField(max_length=15, choices=ETHNICITY_CHOICES, default=False, blank=False)

    def __str__(self):
        return self.first_name


DIET_CHOICES = (('V', 'Veg'), ('N', 'NonVeg'),)


class PatientMedicalCondition(PatientBasicInfo):

    @classmethod
    def create(cls, patient_id):
        patienthist = cls(patient_id=patient_id)
        return patienthist

    def checkFasting(self):
        bmi = float(round((self.weight / (self.height/100) ** 2), 2))
        if (bmi <= 20) or 'kidney' in self.conditions:
            show = 'Based on your Medical History ,you should not be Fasting'
            return show  # False
        else:
            show = 'Based on your Medical History , it is suggested that you follow Intermittent Fasting'
            return show  # True

    DIABETES_CHOICES = (('I', 'Type1'), ('II', 'Type2'),)

    diabetes_type = models.CharField(max_length=2, choices=DIABETES_CHOICES, default=False)
    hba1c_reading = models.CharField(max_length=15, blank=True)
    fasting_reading = models.CharField(max_length=15, blank=True)
    pp_reading = models.CharField(max_length=15, blank=True)

    CONDITIONS_CHOICES = (
        ('hBP', 'HYPERTENSION'),
        ('LBP', 'HYPOTENSION'),
        ('heart', 'HEARTDISEASE'),
        ('kidney', 'KIDNEYDISEASE'),
        ('liver', 'LIVERDISEASE'),
        ('cancer', 'CANCER'),
        ('pcod', 'PCOD'),
        ('pcos', 'PCOS'),
        ('thyroid', 'THYROID'),)

    conditions = MultiSelectField('Medical Conditions', choices=CONDITIONS_CHOICES, null=True, blank=True,
                                  default=False)
    medications = models.TextField(blank=True)
    diet_type = models.CharField(max_length=1, choices=DIET_CHOICES, default=False)
    current_diet = models.TextField(blank=True)
    fasting = models.CharField(max_length=5, blank=True)
    FCONDITIONS_CHOICES = (('diabetes', 'DIABETES'),
                           ('HBP', 'HYPERTENSION'),
                           ('LBP', 'HYPOTENSION'),
                           ('heart', 'HEARTDISEASE'),
                           ('kidney', 'KIDNEYDISEASE'),
                           ('liver', 'LIVERDISEASE'),)

    f_conditions = MultiSelectField('Family Conditions', choices=FCONDITIONS_CHOICES, null=True, blank=True,
                                    default=False)
    family_history = models.TextField(blank=True)
    EXERCISE_CHOICES = (
    ('daily', 'Daily'), ('4-5', '4-5 times a week'), ('2-3', '2-3 times a week'), ('once', 'Once a week'),
    ('No', 'No Exercises'),)
    physical_activities = models.TextField('Exercise Routine', max_length=15, choices=EXERCISE_CHOICES,
                                           default=False)  # ,help_text='Briefly describe your exercise routine')

    def __str__(self):
        return self.first_name


MENU_CHOICES = (
    ('breakfast', 'BREAKFAST'),
    ('lunch', 'LUNCH'),
    ('snack', 'SNACK'),
    ('dinner', 'DINNER'),
)


class Food(models.Model):
    diet_type = models.CharField(max_length=1, choices=DIET_CHOICES, default=False)
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=15, choices=MENU_CHOICES, default=False)

    class Meta:
        abstract = True


class FoodMenu(Food):
    def __str__(self):
        return self.item_type


class PatientMenu(models.Model):
    patient = models.OneToOneField(PatientBasicInfo, on_delete=models.CASCADE, primary_key=True)
    breakfast = models.CharField(max_length=250)
    lunch = models.CharField(max_length=250)
    snack = models.CharField(max_length=250)
    dinner = models.CharField(max_length=250)


    def __str__(self):
        return self.patient

