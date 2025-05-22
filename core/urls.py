from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('vocabulary/', include('core.vocabulary.urls')),
    path('word-alternatives/', views.word_alternatives, name='word_alternatives'),
    path('api/chatbot/', views.process_message, name='process_message'),
    
    # User authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Quiz URLs
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz-results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),
    
    # Vocabulary and progress URLs
    path('favorites/', views.favorites, name='favorites'),
    path('progress/', views.progress, name='progress'),
    
    # AJAX URLs
    path('api/save-word/', views.save_vocabulary_word, name='save_vocabulary_word'),
    path('api/mark-word-mastered/', views.mark_word_mastered, name='mark_word_mastered'),
    path('api/delete-word/', views.delete_saved_word, name='delete_saved_word'),
]
