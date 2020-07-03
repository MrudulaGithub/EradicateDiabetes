from django.contrib import admin
from .models import *


class PatientBasicInfoAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'email_id', 'last_name', 'first_name', 'age', 'gender', 'height', 'weight', 'ethnicity',)


admin.site.register(PatientBasicInfo, PatientBasicInfoAdmin)


class PatientMedicalConditionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'fasting', 'diabetes_type', 'hba1c_reading', 'fasting_reading', 'pp_reading', 'conditions', 'medications','diet_type', 'current_diet', 'f_conditions', 'family_history','physical_activities')


admin.site.register(PatientMedicalCondition, PatientMedicalConditionAdmin)


class PatientMenuAdmin(admin.ModelAdmin):
    list_display = ('patient', 'breakfast', 'lunch', 'snack', 'dinner')


admin.site.register(PatientMenu, PatientMenuAdmin)


class FoodMenuAdmin(admin.ModelAdmin):
    list_display = ('diet_type', 'item_type', 'item_name')
    list_filter = ('diet_type', 'item_type')


admin.site.register(FoodMenu, FoodMenuAdmin)


