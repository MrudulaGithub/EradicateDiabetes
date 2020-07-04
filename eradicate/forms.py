import placeholder
from django.db import models
from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import HiddenInput


class PatientMedicalConditionForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = PatientMedicalCondition
        fields = '__all__'
        exclude = ['patient_id', 'bmi', 'fasting']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),

            'gender': forms.RadioSelect,
            'ethnicity': forms.Select(attrs={'class': 'form-control'}),

            'height': forms.TextInput(attrs={'placeholder': 'in Centimeters', 'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'placeholder': 'in Kgs', 'class': 'form-control'}),
            'diabetes_type': forms.RadioSelect,
            'conditions': forms.CheckboxSelectMultiple,
            'hba1c_reading': forms.TextInput(
                attrs={'placeholder': 'Please mention your hba1c reading', 'class': 'form-control'}),
            'fasting_reading': forms.TextInput(
                attrs={'placeholder': 'Please mention your fasting reading', 'class': 'form-control'}),
            'pp_reading': forms.TextInput(
                attrs={'placeholder': 'Please mention your pp_reading reading', 'class': 'form-control'}),
            'medications': forms.Textarea(
                attrs={'placeholder': 'Please list any medications you currently take', 'class': 'form-control'}),
            'diet_type': forms.RadioSelect,
            'current_diet': forms.Textarea(
                attrs={'placeholder': 'Describe your daily Dietary Habits', 'class': 'form-control'}),
            'f_conditions': forms.CheckboxSelectMultiple,
            'family_history': forms.Textarea(
                attrs={'placeholder': 'Brief description of your family health conditions', 'class': 'form-control'}),
            'physical_activities': forms.RadioSelect,
        }


class PatientMenuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        diet_type = kwargs.pop('diet_type', None)
        super(PatientMenuForm, self).__init__(*args, **kwargs)

        self.fields['breakfast'].choices = [(i, i) for i in FoodMenu.objects.filter(diet_type=diet_type,
                                                                                    item_type='breakfast').values_list(
            'item_name', flat=True)]
        self.fields['lunch'].choices = [(i, i) for i in
                                        FoodMenu.objects.filter(diet_type=diet_type, item_type='lunch').values_list(
                                            'item_name', flat=True)]
        self.fields['snack'].choices = [(i, i) for i in
                                        FoodMenu.objects.filter(diet_type=diet_type, item_type='snack').values_list(
                                            'item_name', flat=True)]
        self.fields['dinner'].choices = [(i, i) for i in
                                         FoodMenu.objects.filter(diet_type=diet_type, item_type='dinner').values_list(
                                             'item_name', flat=True)]

    breakfast = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=True)
    lunch = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=True)
    snack = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=True)
    dinner = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model = PatientMenu
        fields = ['breakfast', 'lunch', 'snack', 'dinner']

