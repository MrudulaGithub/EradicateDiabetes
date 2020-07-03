from django.urls import path
from.import views

app_name = 'eradicate'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:patient_id>/menu/', views.menu, name='menu'),
    path('<int:patient_id>/dietplan/', views.dietplan, name='dietplan'),

]