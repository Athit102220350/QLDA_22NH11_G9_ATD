from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/chatbot/', views.process_message, name='process_message'),
]
