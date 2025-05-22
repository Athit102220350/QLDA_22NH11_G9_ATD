from django.urls import path
from . import views

urlpatterns = [
    path('', views.vocabulary_list_view, name='vocabulary_list'),
    path('save-favorite/', views.save_favorite_word, name='save_favorite_word'),
    path('favorites/', views.favorites_view, name='vocabulary_favorites'),
    path('<str:topic>/', views.vocabulary_topic_view, name='vocabulary_topic'),
]
