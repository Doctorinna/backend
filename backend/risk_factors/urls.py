from django.urls import path
from . import views

urlpatterns = [
    path('diseases/', views.diseases_list, name='diseases'),
    path('categories/', views.categories_list, name='categories'),
    path('questions/', views.questions_list, name='questions'),
    path('questions/<category>', views.questions_list, name='questions'),
    path('response/', views.submit_response, name='response'),
    path('response/<question>', views.change_response, name='response'),
    path('result/', views.get_result, name='result'),
    path('result/<disease>', views.get_result, name='result'),
]
