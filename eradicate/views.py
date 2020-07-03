from django.shortcuts import render, redirect, get_object_or_404
from django.http import request, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import EmailMessage
from .render import Render
import ast
from .models import PatientBasicInfo, PatientMedicalCondition, PatientMenu
from .forms import *
from django.contrib import messages
import boto3
import requests
client = boto3.client('s3')
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        form = PatientMedicalConditionForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=True)
            messages.success(request, 'Your form has been submitted successfully')
            if form['diabetes_type'].value() == 'I':
                return render(request, 'eradicate/Type1.html')
            else:
                return HttpResponseRedirect(reverse('eradicate:menu', args=(patient.pk,)))
    else:
        form = PatientMedicalConditionForm()
        return render(request, 'eradicate/index.html', {'form': form})



def menu(request,patient_id):

    patient_hist = get_object_or_404(PatientMedicalCondition, pk=patient_id)
    patient = get_object_or_404(PatientBasicInfo, pk=patient_id)
    fasting = patient_hist.checkFasting()
    form = PatientMenuForm(diet_type=patient_hist.diet_type)

    #fasting = request.session['fasting']

    if request.method == 'POST':
        form = PatientMenuForm(request.POST, diet_type=patient_hist.diet_type)
        if form.is_valid():
            patientmenu = PatientMenu(patient=patient)

            patientmenu.breakfast = form.cleaned_data['breakfast']
            patientmenu.lunch = form.cleaned_data['lunch']
            patientmenu.snack = form.cleaned_data['snack']
            patientmenu.dinner = form.cleaned_data['dinner']
            patientmenu.save()

            return HttpResponseRedirect(reverse('eradicate:dietplan', args=(patient.pk,)))
    else:
        return render(request, 'eradicate/menu.html', {'form': form, 'patient_id': patient_id, 'fasting': fasting})


def dietplan(request, patient_id):
    patient = get_object_or_404(PatientBasicInfo, pk=patient_id)
    email_id = patient.email_id
    print(email_id)
    patientdiet = get_object_or_404(PatientMenu, pk=patient_id)
    patient_hist = get_object_or_404(PatientMedicalCondition, pk=patient_id)
    fasting = patient_hist.checkFasting()
    #fasting = request.session['fasting']
    fasting_yes = 'Based on your Medical History , it is suggested that you follow Intermittent Fasting'

    # convert string to list output in html -
    bfast = ast.literal_eval(patientdiet.breakfast)
    lunch = ast.literal_eval(patientdiet.lunch)
    snack = ast.literal_eval(patientdiet.snack)
    dinner = ast.literal_eval(patientdiet.dinner)

    context = {
        'bfast': bfast,
        'lunch': lunch,
        'snack': snack,
        'dinner': dinner,
        'patient_id': patient_id,
        'fasting': fasting
    }

    if request.method == 'POST':

        pdf = Render.render('eradicate/dietplan.html', context)

        subject = 'Eradicate Diabetes Diet Plan'
        message = 'Please find attached your customized diet plan and the Eradicate Diabetes diet charts.'
        msg = EmailMessage(subject, message, to=[email_id])
        msg.content_subtype = "html"
        msg.attach('My_Diet.pdf', pdf, 'application/pdf')

        if fasting == fasting_yes:
            msg.attach_file('eradicate\static\eradicate\pdf\Safe Fasting.pdf')
            if patient_hist.diet_type == 'N':
                msg.attach_file('eradicate\static\eradicate\pdf\LCHF Eradicate Diabetes .pdf')
            else:
                msg.attach_file('eradicate\static\eradicate\pdf\LFV Eradicate Diabetes.pdf')
        else:
            if patient_hist.diet_type == 'N':
                msg.attach_file('eradicate\static\eradicate\pdf\LCHF Eradicate Diabetes .pdf')
            else:
                msg.attach_file('eradicate\static\eradicate\pdf\LFV Eradicate Diabetes.pdf')

        msg.send()
        messages.success(request, 'Thank you, an email with your diet has been sent to you')

    return render(request, 'eradicate/dietplan.html', context)

