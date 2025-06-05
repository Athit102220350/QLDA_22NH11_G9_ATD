from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone
import json
from django.contrib import admin
# Create your models here.
class UserProfile(models.Model):
    """Extended user profile for learning data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    level = models.CharField(max_length=20, default='beginner', 
                             choices=[('beginner', 'Beginner'), 
                                      ('intermediate', 'Intermediate'), 
                                      ('advanced', 'Advanced')])
    interests = models.CharField(max_length=255, blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class LearningProgress(models.Model):
    """Track user's learning progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')  
    activity_type = models.CharField(max_length=50, 
                                    choices=[('grammar', 'Grammar'), 
                                             ('vocabulary', 'Vocabulary'), 
                                             ('quiz', 'Quiz')])
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username}'s {self.activity_type} progress on {self.timestamp.strftime('%Y-%m-%d')}"


# class SavedWord(models.Model):
#     """Words saved by users for later study"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_words')
#     word = models.CharField(max_length=100)
#     definition = models.TextField()
#     example = models.TextField(blank=True, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#     mastered = models.BooleanField(default=False)
    
#     class Meta:
#         unique_together = ('user', 'word')
#         ordering = ['-date_added']
    
#     def __str__(self):
#         return f"{self.user.username} - {self.word}"
class SavedWord(models.Model):
    """Words saved by users for later study"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_words')
    word = models.CharField(max_length=100)
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    mastered = models.BooleanField(default=False)
    
    # New fields
    topic = models.CharField(max_length=100, blank=True, null=True, choices=[
        ('business', 'Business'),
        ('sport', 'Sport'),
        ('politics', 'Politics'),
        ('technology', 'Technology'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('entertainment', 'Entertainment'),
        ('science', 'Science'),
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('other', 'Other')
    ])
    
    level = models.CharField(max_length=20, blank=True, null=True,
                            choices=[('beginner', 'Beginner'),
                                    ('intermediate', 'Intermediate'),
                                    ('advanced', 'Advanced')])
    
    part_of_speech = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('adjective', 'Adjective'),
        ('adverb', 'Adverb'),
        ('pronoun', 'Pronoun'),
        ('preposition', 'Preposition'),
        ('conjunction', 'Conjunction'),
        ('interjection', 'Interjection'),
        ('determiner', 'Determiner')
    ])
    
    synonyms = models.TextField(blank=True, null=True, help_text="Comma-separated synonyms")
    pronunciation = models.CharField(max_length=100, blank=True, null=True)
    audio = models.FileField(upload_to='vocabulary_audio/', blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'word')
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.user.username} - {self.word}"

class CompletedLesson(models.Model):
    """Track completed lessons"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_lessons')
    lesson_name = models.CharField(max_length=100)
    completed_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'lesson_name')
        ordering = ['-completed_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson_name}"


class Quiz(models.Model):
    """Model for quizzes"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20,
                                 choices=[('beginner', 'Beginner'),
                                          ('intermediate', 'Intermediate'),
                                          ('advanced', 'Advanced')])
    created_date = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=600, help_text="Time limit in seconds (default: 10 minutes)")
    pass_mark = models.IntegerField(default=60, help_text="Percentage score needed to pass")
    category = models.CharField(max_length=50, default='general',
                              choices=[('grammar', 'Grammar'),
                                      ('vocabulary', 'Vocabulary'),
                                      ('reading', 'Reading Comprehension'),
                                      ('listening', 'Listening Comprehension'),
                                      ('general', 'General English')])
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['difficulty', 'title']
    
    def __str__(self):
        return self.title
    
    def get_questions(self):
        return self.questions.all()[:5]  # Limit to 5 questions
    
    def get_question_count(self):
        return self.questions.count()
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('take_quiz', args=[str(self.id)])


class QuizQuestion(models.Model):
    """Model for quiz questions"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    # Optional context for reading-based questions
    context = models.TextField(blank=True, null=True)
    # Audio file for listening questions
    audio_file = models.FileField(upload_to='quiz_audio/', blank=True, null=True)
    
    def __str__(self):
        return self.question_text[:50]
    
    def get_answers(self):
        return self.answers.all()


class QuizAnswer(models.Model):
    """Model for quiz answers"""
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.answer_text} ({'Correct' if self.is_correct else 'Incorrect'})"


class QuizAttempt(models.Model):
    """Model to track quiz attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)    
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_started = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_started']
    
    def __str__(self):
        return f"{self.user.username}'s attempt on {self.quiz.title}"


class Vocabulary(models.Model):
    """Model for vocabulary words"""
    word = models.CharField(max_length=100)
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)
    pronunciation = models.CharField(max_length=100, blank=True, null=True)
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20,
                                 choices=[('beginner', 'Beginner'),
                                          ('intermediate', 'Intermediate'),
                                          ('advanced', 'Advanced')],
                                 default='beginner')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Vocabularies"
        ordering = ['word']
    
    def __str__(self):
        return f"{self.word} ({self.topic})"


class FavoriteVocabulary(models.Model):
    """Model for users' favorite vocabulary words"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_words')
    word = models.CharField(max_length=100)
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    mastered = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Favorite Vocabularies"
        unique_together = ('user', 'word')
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.user.username} - {self.word}"


class QuizProgress(models.Model):
    """Model to track user's progress across all quizzes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_progress')
    category = models.CharField(max_length=50, choices=[
        ('grammar', 'Grammar'),
        ('vocabulary', 'Vocabulary'),
        ('reading', 'Reading Comprehension'),
        ('listening', 'Listening Comprehension'),
        ('general', 'General English')
    ])
    total_attempted = models.IntegerField(default=0)
    total_completed = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'category')
    
    def __str__(self):
        return f"{self.user.username}'s {self.category} progress"
        
    def update_progress(self):
        """Update progress stats based on user's quiz attempts"""
        # Get all completed attempts in this category
        category_attempts = QuizAttempt.objects.filter(
            user=self.user,
            quiz__category=self.category,
            completed=True
        )
        
        # Update statistics
        self.total_completed = category_attempts.count()
        self.total_attempted = QuizAttempt.objects.filter(
            user=self.user,
            quiz__category=self.category
        ).count()
        
        if self.total_completed > 0:
            self.average_score = category_attempts.aggregate(Avg('score'))['score__avg']
        else:
            self.average_score = 0
            
        self.save()

class MockTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=50)  # e.g., 'toeic', 'cambridge'
    topic = models.CharField(max_length=50)      # e.g., 'business', 'technology'
    score = models.PositiveIntegerField()        # overall percentage score
    correct_answers = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    level_achieved = models.CharField(max_length=5, default='A1')  # Add default='A1' here
    user_answers = models.TextField(default="{}")  # JSON string storing user's answers
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.test_type} test - {self.score}%"
    
    def get_section_scores(self):
        """Calculate scores for each section"""
        try:
            # Parse user answers from JSON
            user_answers = json.loads(self.user_answers)
            
            # Get the test data
            from .mock_data.test_data import MOCK_TEST_DATA
            test_data = MOCK_TEST_DATA[self.test_type][self.topic]
            
            # Initialize section scores
            section_scores = {
                'reading': {'score': 0, 'total': 0, 'percentage': 0},
                'grammar': {'score': 0, 'total': 0, 'percentage': 0},
                'vocabulary': {'score': 0, 'total': 0, 'percentage': 0}
            }
            
            # Calculate reading scores
            for reading in test_data['reading']:
                for i, question in enumerate(reading['questions']):
                    answer_key = f"reading_{reading['id']}_q{i}"
                    if answer_key in user_answers:
                        section_scores['reading']['total'] += 1
                        if int(user_answers[answer_key]) == question['correct']:
                            section_scores['reading']['score'] += 1
            
            # Calculate grammar scores
            for grammar in test_data['grammar']:
                answer_key = f"grammar_{grammar['id']}"
                if answer_key in user_answers:
                    section_scores['grammar']['total'] += 1
                    if int(user_answers[answer_key]) == grammar['correct']:
                        section_scores['grammar']['score'] += 1
            
            # Calculate vocabulary scores
            for vocab in test_data['vocabulary']:
                answer_key = f"vocabulary_{vocab['id']}"
                if answer_key in user_answers:
                    section_scores['vocabulary']['total'] += 1
                    if int(user_answers[answer_key]) == vocab['correct']:
                        section_scores['vocabulary']['score'] += 1
            
            # Calculate percentages
            for section in section_scores:
                if section_scores[section]['total'] > 0:
                    section_scores[section]['percentage'] = round(
                        (section_scores[section]['score'] / section_scores[section]['total']) * 100
                    )
            
            return section_scores
        except Exception as e:
            # Return default section scores if there's an error
            return {
                'reading': {'score': 0, 'total': 0, 'percentage': 0},
                'grammar': {'score': 0, 'total': 0, 'percentage': 0},
                'vocabulary': {'score': 0, 'total': 0, 'percentage': 0}
            }

    def get_suggestions(self):
        """Generate study suggestions based on test results"""
        section_scores = self.get_section_scores()
        
        suggestions = {
            'general': '',
            'sections': {}
        }
        
        # General suggestions based on overall score
        if self.score < 40:
            suggestions['general'] = "Focus on building your foundational English skills. Consider starting with basic grammar rules and vocabulary."
        elif self.score < 70:
            suggestions['general'] = "You have a good foundation. Work on expanding your vocabulary and practicing more complex grammar structures."
        else:
            suggestions['general'] = "You've demonstrated strong English skills. Continue to refine your knowledge with advanced reading materials and practice expressing complex ideas."
        
        # Section-specific suggestions
        for section, data in section_scores.items():
            if data['percentage'] < 50:
                if section == 'reading':
                    suggestions['sections'][section] = "Practice reading comprehension with varied texts. Focus on identifying main ideas and supporting details."
                elif section == 'grammar':
                    suggestions['sections'][section] = "Review basic grammar rules and practice with exercises focusing on sentence structure and verb tenses."
                else:  # vocabulary
                    suggestions['sections'][section] = "Build your vocabulary by learning new words in context through reading and listening to English content."
            elif data['percentage'] < 80:
                if section == 'reading':
                    suggestions['sections'][section] = "Enhance your reading skills by practicing with more complex texts and focusing on inference and analysis."
                elif section == 'grammar':
                    suggestions['sections'][section] = "Continue practicing with intermediate grammar exercises, focusing on areas like conditionals and passive voice."
                else:  # vocabulary
                    suggestions['sections'][section] = "Expand your vocabulary by learning synonyms, antonyms, and context-specific usage of words."
            else:
                if section == 'reading':
                    suggestions['sections'][section] = "Challenge yourself with advanced academic or technical texts to further refine your reading comprehension."
                elif section == 'grammar':
                    suggestions['sections'][section] = "Focus on mastering complex grammar structures and nuances in language usage."
                else:  # vocabulary
                    suggestions['sections'][section] = "Work on specialized vocabulary in areas of your interest to become more fluent in specific contexts."
        
        return suggestions
    
@admin.register(MockTestResult)
class MockTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_type', 'topic', 'score', 'level_achieved', 'created_at')
    list_filter = ('test_type', 'topic', 'level_achieved')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'