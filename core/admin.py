from django.contrib import admin
from .models import (UserProfile, LearningProgress, SavedWord, 
                     CompletedLesson, Quiz, QuizQuestion, 
                     QuizAnswer, QuizAttempt, Vocabulary, FavoriteVocabulary, QuizProgress)

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'joined_date')
    search_fields = ('user__username', 'user__email')
    list_filter = ('level',)

@admin.register(SavedWord)
class SavedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'user', 'date_added', 'mastered')
    list_filter = ('mastered', 'date_added')
    search_fields = ('word', 'user__username')

# Inline admin for quiz answers
class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 4
    fields = ['answer_text', 'is_correct']

# Inline admin for quiz questions
class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 1
    fields = ['question_text', 'context']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_date', 'question_count')
    list_filter = ('difficulty', 'created_date')
    search_fields = ('title', 'description')
    inlines = [QuizQuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    
    question_count.short_description = 'Number of Questions'

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'answer_count')
    list_filter = ('quiz__difficulty',)
    search_fields = ('question_text', 'quiz__title')
    inlines = [QuizAnswerInline]
    
    def answer_count(self, obj):
        return obj.answers.count()
    
    answer_count.short_description = 'Number of Answers'

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed', 'date_started', 'date_completed')
    list_filter = ('completed', 'date_started', 'quiz__difficulty')
    search_fields = ('user__username', 'quiz__title')
    
@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'score', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username', 'details')

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson_name', 'score', 'completed_date')
    list_filter = ('completed_date',)
    search_fields = ('user__username', 'lesson_name')

@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ('word', 'topic', 'difficulty', 'date_added')
    list_filter = ('topic', 'difficulty', 'date_added')
    search_fields = ('word', 'definition')

@admin.register(FavoriteVocabulary)
class FavoriteVocabularyAdmin(admin.ModelAdmin):
    list_display = ('word', 'user', 'date_added', 'mastered')
    list_filter = ('mastered', 'date_added')
    search_fields = ('word', 'user__username')

@admin.register(QuizProgress)
class QuizProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'total_completed', 'average_score', 'last_updated')
    list_filter = ('category', 'last_updated')
    search_fields = ('user__username',)
