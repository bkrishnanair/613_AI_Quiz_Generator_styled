# Quiz_Base/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
]
