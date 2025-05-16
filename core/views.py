from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from core.ai.huggingface_integration import grammar_corrector, vocabulary_enhancer
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileUpdateForm, UserUpdateForm
from .models import (UserProfile, LearningProgress, SavedWord, CompletedLesson, 
                    Quiz, QuizQuestion, QuizAnswer, QuizAttempt)

# Create your views here.
def index(request):
    """View for the homepage."""
    return render(request, 'index.html')

def chatbot(request):
    """View for the chatbot page."""
    return render(request, 'chatbot.html')

def vocabulary(request):
    """View for the vocabulary learning page."""
    return render(request, 'vocabulary.html')

def word_alternatives(request):
    """View for the word alternatives page."""
    return render(request, 'word_alternatives.html')

def register(request):
    """View for user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to English Learning Website.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """View for user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """View for user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')

@login_required
def dashboard(request):
    """View for user dashboard."""
    user = request.user
    
    # Get user progress statistics
    learning_progress = LearningProgress.objects.filter(user=user).order_by('-timestamp')[:5]
    saved_words = SavedWord.objects.filter(user=user)
    completed_lessons = CompletedLesson.objects.filter(user=user)
    
    context = {
        'user': user,
        'learning_progress': learning_progress,
        'saved_words': saved_words,
        'completed_lessons': completed_lessons,
        'word_count': saved_words.count(),
        'lesson_count': completed_lessons.count(),
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    """View for user profile update."""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'profile.html', context)

@csrf_exempt
def process_message(request):
    """Handle chatbot API interaction."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            message_type = data.get('type', 'grammar')  # Default to grammar
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Determine the type of request and use the appropriate AI model
            response_data = {}
            
            if message_type == 'grammar':
                # Use Hugging Face grammar correction
                correction_result = grammar_corrector.correct_grammar(user_message)
                
                response_data = {
                    'response_type': 'grammar',
                    'original_text': user_message,
                    'corrected_text': correction_result['corrected_text'],
                    'has_errors': correction_result['has_errors'],
                    'explanation': correction_result['explanation']
                }
                
            elif message_type == 'vocabulary':
                # Get word from the message
                words = user_message.strip().split()
                if words:
                    word_to_lookup = words[0].lower().strip('.,;:!?()"\'')
                    word_info = vocabulary_enhancer.get_word_info(word_to_lookup)
                    
                    response_data = {
                        'response_type': 'vocabulary',
                        'word': word_to_lookup,
                        'definition': word_info.get('definition', 'Definition not available'),
                        'example': word_info.get('example', 'Example not available'),
                        'synonyms': word_info.get('synonyms', [])
                    }
                else:
                    response_data = {
                        'response_type': 'error',
                        'message': 'No word provided for vocabulary lookup'
                    }
                    
            elif message_type == 'alternatives':
                # Get word and context
                parts = user_message.split('in', 1)
                if len(parts) > 1:
                    word = parts[0].strip()
                    context = parts[1].strip()
                    alternatives = vocabulary_enhancer.suggest_alternative_words(word, context)
                    
                    response_data = {
                        'response_type': 'alternatives',
                        'word': word,
                        'context': context,
                        'alternatives': alternatives.get('alternatives', [])
                    }
                else:
                    response_data = {
                        'response_type': 'error',
                        'message': 'Please provide a word and context using format: "word in context"'
                    }
            else:
                # Fallback to simple response
                response_data = {
                    'response_type': 'simple',
                    'response': f"I received your message: '{user_message}'"
                }
                
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@login_required
def quiz_list(request):
    """View for displaying available quizzes."""
    quizzes = Quiz.objects.all()
    
    # Get the user's quiz attempts
    user_attempts = QuizAttempt.objects.filter(user=request.user)
    
    # Create a dictionary of quiz attempts for each quiz
    attempts_dict = {}
    for attempt in user_attempts:
        if attempt.quiz.id not in attempts_dict or attempt.date_started > attempts_dict[attempt.quiz.id]['date']:
            attempts_dict[attempt.quiz.id] = {
                'score': attempt.score,
                'date': attempt.date_started,
                'completed': attempt.completed
            }
    
    context = {
        'quizzes': quizzes,
        'attempts_dict': attempts_dict
    }
    
    return render(request, 'quiz_list.html', context)

@login_required
def take_quiz(request, quiz_id):
    """View for taking a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check if there's an unfinished attempt
    existing_attempt = QuizAttempt.objects.filter(
        user=request.user, 
        quiz=quiz, 
        completed=False
    ).first()
    
    if not existing_attempt:
        # Create a new attempt
        existing_attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz
        )
    
    if request.method == 'POST':
        # Process quiz submission
        score = 0
        total_questions = 0
        
        for question in quiz.get_questions():
            total_questions += 1
            answer_id = request.POST.get(f'question_{question.id}')
            
            if answer_id:
                selected_answer = QuizAnswer.objects.get(id=answer_id)
                if selected_answer.is_correct:
                    score += 1
        
        # Calculate percentage score
        percentage_score = int((score / total_questions) * 100) if total_questions > 0 else 0
        
        # Update the attempt
        existing_attempt.score = percentage_score
        existing_attempt.completed = True
        existing_attempt.date_completed = timezone.now()
        existing_attempt.save()
        
        # Create a learning progress record
        LearningProgress.objects.create(
            user=request.user,
            activity_type='quiz',
            score=percentage_score,
            details=f"Completed quiz: {quiz.title}"
        )
        
        # Check if this quiz completion should be counted as a lesson
        CompletedLesson.objects.get_or_create(
            user=request.user,
            lesson_name=f"Quiz: {quiz.title}",
            defaults={'score': percentage_score}
        )
        
        messages.success(request, f'Quiz completed with score: {percentage_score}%')
        return redirect('quiz_results', attempt_id=existing_attempt.id)
    
    context = {
        'quiz': quiz,
        'questions': quiz.get_questions(),
        'attempt': existing_attempt
    }
    
    return render(request, 'take_quiz.html', context)

@login_required
def quiz_results(request, attempt_id):
    """View for displaying quiz results."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if not attempt.completed:
        messages.warning(request, 'This quiz attempt has not been completed yet.')
        return redirect('take_quiz', quiz_id=attempt.quiz.id)
    
    context = {
        'attempt': attempt,
        'quiz': attempt.quiz
    }
    
    return render(request, 'quiz_results.html', context)

@login_required
def favorites(request):
    """View for displaying user's saved vocabulary words."""
    saved_words = SavedWord.objects.filter(user=request.user)
    
    context = {
        'saved_words': saved_words
    }
    
    return render(request, 'favorites.html', context)

@login_required
def progress(request):
    """View for displaying user's learning progress."""
    # Get all learning progress records
    all_progress = LearningProgress.objects.filter(user=request.user)
    
    # Get quiz attempts
    quiz_attempts = QuizAttempt.objects.filter(user=request.user, completed=True)
    
    # Get completed lessons
    completed_lessons = CompletedLesson.objects.filter(user=request.user)
      # Calculate statistics
    total_activities = all_progress.count()
    avg_score = all_progress.aggregate(Avg('score'))['score__avg'] or 0
    avg_score = round(avg_score, 1)
    
    # Group progress by activity type for chart
    activity_data = {}
    for progress in all_progress:
        if progress.activity_type not in activity_data:
            activity_data[progress.activity_type] = []
        
        activity_data[progress.activity_type].append({
            'date': progress.timestamp.strftime('%Y-%m-%d'),
            'score': progress.score
        })
    
    context = {
        'all_progress': all_progress[:10],  # Show only 10 most recent
        'quiz_attempts': quiz_attempts,
        'completed_lessons': completed_lessons,
        'total_activities': total_activities,
        'avg_score': avg_score,
        'activity_data': json.dumps(activity_data)
    }
    
    return render(request, 'progress.html', context)

@csrf_exempt
@login_required
def save_vocabulary_word(request):
    """AJAX view for saving a vocabulary word to user's list."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word = data.get('word', '').strip()
            definition = data.get('definition', '')
            example = data.get('example', '')
            
            if not word or not definition:
                return JsonResponse({'success': False, 'error': 'Word and definition are required'})
            
            # Save or update the word
            saved_word, created = SavedWord.objects.get_or_create(
                user=request.user,
                word=word,
                defaults={
                    'definition': definition,
                    'example': example
                }
            )
            
            if not created:
                # Update the definition and example if the word already exists
                saved_word.definition = definition
                saved_word.example = example
                saved_word.save()
            
            return JsonResponse({
                'success': True, 
                'created': created,
                'word_id': saved_word.id,
                'message': 'Word added to your vocabulary list!' if created else 'Word updated in your vocabulary list!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})

@csrf_exempt
@login_required
def mark_word_mastered(request):
    """AJAX view for marking a vocabulary word as mastered."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word_id = data.get('word_id')
            
            if not word_id:
                return JsonResponse({'success': False, 'error': 'Word ID is required'})
            
            # Get the word and update mastered status
            saved_word = get_object_or_404(SavedWord, id=word_id, user=request.user)
            saved_word.mastered = not saved_word.mastered  # Toggle mastered status
            saved_word.save()
            
            return JsonResponse({
                'success': True, 
                'word_id': saved_word.id,
                'mastered': saved_word.mastered,
                'message': f"Word marked as {'mastered' if saved_word.mastered else 'not mastered'}"
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})

@csrf_exempt
@login_required
def delete_saved_word(request):
    """AJAX view for deleting a saved vocabulary word."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            word_id = data.get('word_id')
            
            if not word_id:
                return JsonResponse({'success': False, 'error': 'Word ID is required'})
            
            # Delete the word
            saved_word = get_object_or_404(SavedWord, id=word_id, user=request.user)
            word_text = saved_word.word
            saved_word.delete()
            
            return JsonResponse({
                'success': True, 
                'message': f"Word '{word_text}' removed from your vocabulary list"
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'})
