import random
from django.core.management.base import BaseCommand
from core.models import Quiz, QuizQuestion, QuizAnswer

class Command(BaseCommand):
    help = 'Adds sample quizzes for English learning'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample quizzes...')
          # Create sample beginner level grammar quiz
        grammar_quiz = Quiz.objects.create(
            title='Basic English Grammar',
            description='Test your knowledge of basic English grammar rules including tenses, articles, and prepositions.',
            difficulty='beginner',
            category='grammar',
            time_limit=600,  # 10 minutes
            pass_mark=70
        )
        
        # Create sample questions for grammar quiz
        q1 = QuizQuestion.objects.create(
            quiz=grammar_quiz,
            question_text='Which sentence uses the present continuous tense correctly?'
        )
        QuizAnswer.objects.create(question=q1, answer_text='I am going to the store tomorrow.', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='She watching TV right now.', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='They are studying for their exam.', is_correct=True)
        QuizAnswer.objects.create(question=q1, answer_text='He work at the office every day.', is_correct=False)
        
        q2 = QuizQuestion.objects.create(
            quiz=grammar_quiz,
            question_text='Choose the sentence with the correct article usage:'
        )
        QuizAnswer.objects.create(question=q2, answer_text='I saw a elephant at the zoo.', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='She is the best student in an class.', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='He bought a new car last month.', is_correct=True)
        QuizAnswer.objects.create(question=q2, answer_text='They went to the university in hour ago.', is_correct=False)
        
        q3 = QuizQuestion.objects.create(
            quiz=grammar_quiz,
            question_text='Which sentence contains a preposition error?'
        )
        QuizAnswer.objects.create(question=q3, answer_text='She arrived at the airport on time.', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='We re going to the movies in Saturday.', is_correct=True)
        QuizAnswer.objects.create(question=q3, answer_text='The book is on the table.', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='They walked through the park.', is_correct=False)
        
        q4 = QuizQuestion.objects.create(
            quiz=grammar_quiz,
            question_text='Select the correct past tense form of the verb "go":'
        )
        QuizAnswer.objects.create(question=q4, answer_text='goed', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='went', is_correct=True)
        QuizAnswer.objects.create(question=q4, answer_text='gone', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='going', is_correct=False)
        
        q5 = QuizQuestion.objects.create(
            quiz=grammar_quiz,
            question_text='Which sentence uses the correct plural form?'
        )
        QuizAnswer.objects.create(question=q5, answer_text='I have two childs.', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='There are five sheep in the field.', is_correct=True)
        QuizAnswer.objects.create(question=q5, answer_text='We saw many mouses in the barn.', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='They have three foots.', is_correct=False)
          # Create sample intermediate vocabulary quiz
        vocab_quiz = Quiz.objects.create(
            title='English Vocabulary Challenge',
            description='Expand your English vocabulary with this quiz on synonyms, antonyms, and definitions.',
            difficulty='intermediate',
            category='vocabulary',
            time_limit=720,  # 12 minutes
            pass_mark=60
        )
        
        # Create sample questions for vocabulary quiz
        q1 = QuizQuestion.objects.create(
            quiz=vocab_quiz,
            question_text='What is the best synonym for "jubilant"?'
        )
        QuizAnswer.objects.create(question=q1, answer_text='Angry', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='Sad', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='Ecstatic', is_correct=True)
        QuizAnswer.objects.create(question=q1, answer_text='Tired', is_correct=False)
        
        q2 = QuizQuestion.objects.create(
            quiz=vocab_quiz,
            question_text='Choose the antonym of "frugal":'
        )
        QuizAnswer.objects.create(question=q2, answer_text='Thrifty', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='Extravagant', is_correct=True)
        QuizAnswer.objects.create(question=q2, answer_text='Economical', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='Careful', is_correct=False)
        
        q3 = QuizQuestion.objects.create(
            quiz=vocab_quiz,
            question_text='What does "ameliorate" mean?'
        )
        QuizAnswer.objects.create(question=q3, answer_text='To make worse', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='To make better or improve', is_correct=True)
        QuizAnswer.objects.create(question=q3, answer_text='To destroy completely', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='To remain neutral', is_correct=False)
        
        q4 = QuizQuestion.objects.create(
            quiz=vocab_quiz,
            question_text='Which word is closest in meaning to "pernicious"?'
        )
        QuizAnswer.objects.create(question=q4, answer_text='Beneficial', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='Harmless', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='Harmful', is_correct=True)
        QuizAnswer.objects.create(question=q4, answer_text='Powerless', is_correct=False)
        
        q5 = QuizQuestion.objects.create(
            quiz=vocab_quiz,
            question_text='What is a "conundrum"?'
        )
        QuizAnswer.objects.create(question=q5, answer_text='A type of musical instrument', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='A difficult problem or puzzle', is_correct=True)
        QuizAnswer.objects.create(question=q5, answer_text='A large building', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='A celebration or festival', is_correct=False)
          # Create sample advanced reading comprehension quiz
        reading_quiz = Quiz.objects.create(
            title='Reading Comprehension',
            description='Test your advanced reading comprehension skills with passages and analytical questions.',
            difficulty='advanced',
            category='reading',
            time_limit=900,  # 15 minutes
            pass_mark=50
        )
        
        # Create sample reading comprehension questions
        passage = """
        The concept of sustainable development has gained widespread acceptance in recent decades as humanity grapples with increasingly complex environmental challenges. At its core, sustainability seeks to meet the needs of the present without compromising the ability of future generations to meet their own needs. This principle requires balancing economic growth, social equity, and environmental protection—often referred to as the "triple bottom line." 
        
        However, implementing sustainable practices across global economic systems has proven challenging. Developed nations, having built their wealth through centuries of unconstrained resource consumption, now face the difficult task of transitioning to greener economies while maintaining prosperity. Meanwhile, developing countries rightfully assert their need for economic growth to alleviate poverty, even as they face pressure to leapfrog directly to sustainable models.
        
        Climate change further complicates this delicate balance. As scientific consensus confirms the human impact on global warming, nations must collaborate on unprecedented scales while navigating complex geopolitical interests. The Paris Agreement represents a significant, if imperfect, step toward collective action, but questions remain about whether such frameworks can drive change quickly enough to prevent irreversible environmental damage.
        """
        
        q1 = QuizQuestion.objects.create(
            quiz=reading_quiz,
            question_text='According to the passage, what is the "triple bottom line" of sustainability?',
            context=passage
        )
        QuizAnswer.objects.create(question=q1, answer_text='Past, present, and future needs', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='Local, national, and global considerations', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='Economic growth, social equity, and environmental protection', is_correct=True)
        QuizAnswer.objects.create(question=q1, answer_text='Developed, developing, and underdeveloped nations', is_correct=False)
        
        q2 = QuizQuestion.objects.create(
            quiz=reading_quiz,
            question_text='What challenge do developing countries face regarding sustainability, according to the passage?',
            context=passage
        )
        QuizAnswer.objects.create(question=q2, answer_text='They lack the technological capability to implement sustainable practices', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='They need economic growth to reduce poverty while facing pressure to adopt sustainable models', is_correct=True)
        QuizAnswer.objects.create(question=q2, answer_text='They have no interest in environmental protection', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='They cannot participate in international agreements like the Paris Agreement', is_correct=False)
        
        q3 = QuizQuestion.objects.create(
            quiz=reading_quiz,
            question_text='The overall tone of the passage can best be described as:',
            context=passage
        )
        QuizAnswer.objects.create(question=q3, answer_text='Optimistic about solving environmental problems', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='Critical of international cooperation efforts', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='Analytical and cautiously concerned', is_correct=True)
        QuizAnswer.objects.create(question=q3, answer_text='Despairing about the future of humanity', is_correct=False)
        
        q4 = QuizQuestion.objects.create(
            quiz=reading_quiz,
            question_text='What does the passage suggest about developed nations?',
            context=passage
        )
        QuizAnswer.objects.create(question=q4, answer_text='They bear no responsibility for current environmental problems', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='They built their wealth through unsustainable resource use and now face transition challenges', is_correct=True)
        QuizAnswer.objects.create(question=q4, answer_text='They have successfully implemented sustainable economies', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='They should dictate environmental policy to developing nations', is_correct=False)
        
        q5 = QuizQuestion.objects.create(
            quiz=reading_quiz,
            question_text='The Paris Agreement is characterized in the passage as:',            context=passage
        )
        QuizAnswer.objects.create(question=q5, answer_text='A complete failure', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='The perfect solution to climate change', is_correct=False)        
        QuizAnswer.objects.create(question=q5, answer_text='An imperfect but significant step toward collective action', is_correct=True)
        QuizAnswer.objects.create(question=q5, answer_text='Irrelevant to developing nations', is_correct=False)
        
        # Create sample listening comprehension quiz
        listening_quiz = Quiz.objects.create(
            title='Listening Comprehension',
            description='Test your listening comprehension skills with audio clips and questions.',
            difficulty='intermediate',
            category='listening',
            time_limit=480,  # 8 minutes
            pass_mark=60
        )
        
        # Create sample listening comprehension questions
        context = "This quiz is based on audio clips that would be played in a real quiz. For this sample, read the transcript and answer the questions."
        
        audio_transcript = """
        Interviewer: Today we're speaking with Dr. Jane Carter, an expert on climate change. Dr. Carter, can you explain why small temperature changes matter so much?
        
        Dr. Carter: Certainly. When we talk about a global temperature increase of 1.5 or 2 degrees Celsius, it doesn't sound like much, but it represents an enormous amount of energy in the Earth's climate system. Even half a degree can make a significant difference in sea levels, weather patterns, and ecosystem health. Think of it like human body temperature - a fever of just 2 degrees can make you quite ill.
        
        Interviewer: What actions should ordinary people take to help address climate change?
        
        Dr. Carter: Individual actions do matter, but they work best alongside systemic change. Reducing meat consumption, especially beef, can lower your carbon footprint. Using public transportation or cycling instead of driving helps too. But equally important is voting for climate-conscious policies and supporting companies with sustainable practices. We need both personal and collective action.
        """
        
        q1 = QuizQuestion.objects.create(
            quiz=listening_quiz,
            question_text='According to Dr. Carter, why are small temperature changes significant?',
            context=f"{context}\n\nTranscript:\n{audio_transcript}"
        )
        QuizAnswer.objects.create(question=q1, answer_text='Because scientists have exaggerated their importance', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='Because they represent enormous amounts of energy in the climate system', is_correct=True)
        QuizAnswer.objects.create(question=q1, answer_text='Because the Earth naturally varies by several degrees every year', is_correct=False)
        QuizAnswer.objects.create(question=q1, answer_text='Because temperature measurements are often inaccurate', is_correct=False)
        
        q2 = QuizQuestion.objects.create(
            quiz=listening_quiz,
            question_text='What analogy does Dr. Carter use to explain global temperature changes?',
            context=f"{context}\n\nTranscript:\n{audio_transcript}"
        )
        QuizAnswer.objects.create(question=q2, answer_text='Cooking temperatures', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='Engine overheating', is_correct=False)
        QuizAnswer.objects.create(question=q2, answer_text='Human body temperature and fever', is_correct=True)
        QuizAnswer.objects.create(question=q2, answer_text='Ice melting points', is_correct=False)
        
        q3 = QuizQuestion.objects.create(
            quiz=listening_quiz,
            question_text='What does Dr. Carter suggest people can do to reduce their carbon footprint?',
            context=f"{context}\n\nTranscript:\n{audio_transcript}"
        )
        QuizAnswer.objects.create(question=q3, answer_text='Install solar panels', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='Reduce meat consumption and use public transportation', is_correct=True)
        QuizAnswer.objects.create(question=q3, answer_text='Move to colder climates', is_correct=False)
        QuizAnswer.objects.create(question=q3, answer_text='Buy more efficient air conditioners', is_correct=False)
        
        q4 = QuizQuestion.objects.create(
            quiz=listening_quiz,
            question_text='According to Dr. Carter, which type of action is most important?',
            context=f"{context}\n\nTranscript:\n{audio_transcript}"
        )
        QuizAnswer.objects.create(question=q4, answer_text='Only individual actions matter', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='Only systemic changes matter', is_correct=False)
        QuizAnswer.objects.create(question=q4, answer_text='Both personal and collective action are important', is_correct=True)
        QuizAnswer.objects.create(question=q4, answer_text='Government regulation is the only solution', is_correct=False)
        
        q5 = QuizQuestion.objects.create(
            quiz=listening_quiz,
            question_text='Who is being interviewed in this audio clip?',
            context=f"{context}\n\nTranscript:\n{audio_transcript}"
        )
        QuizAnswer.objects.create(question=q5, answer_text='A politician', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='A climate change activist', is_correct=False)
        QuizAnswer.objects.create(question=q5, answer_text='Dr. Jane Carter, a climate change expert', is_correct=True)
        QuizAnswer.objects.create(question=q5, answer_text='A public transportation advocate', is_correct=False)
        
        self.stdout.write(self.style.SUCCESS('Successfully created sample quizzes!'))
