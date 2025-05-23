from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

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


class SavedWord(models.Model):
    """Words saved by users for later study"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_words')
    word = models.CharField(max_length=100)
    definition = models.TextField()
    example = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    mastered = models.BooleanField(default=False)
    
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
