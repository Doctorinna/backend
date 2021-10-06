from django.urls import path
from . import views

urlpatterns = [
    path('diseases/', views.diseases_list, name='diseases'),
    path('questions/', views.questions_list, name='questions'),
]
