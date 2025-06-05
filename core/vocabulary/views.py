from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from core.models import SavedWord
import json
import string
import random
import requests
from collections import defaultdict

# Use SavedWord model for vocabulary functionality
Vocabulary = SavedWord
FavoriteVocabulary = SavedWord

# Define topics with difficulty levels
TOPIC_WORDS = {
    'business': [('company', 'A2'), ('finance', 'B1'), ('market', 'B1'), ('entrepreneur', 'B2'), ('investment', 'B2'), ('revenue', 'C1'), ('merger', 'C1'), ('diversification', 'C2'), ('arbitrage', 'C2')],
    'sport': [('athlete', 'B1'), ('competition', 'A2'), ('tournament', 'B2'), ('championship', 'B2'), ('fitness', 'A2'), ('endurance', 'B2'), ('coach', 'B1'), ('sportsmanship', 'C2'), ('adversity', 'C2')],
    'politician': [('government', 'A2'), ('election', 'B1'), ('campaign', 'B2'), ('policy', 'B2'), ('debate', 'B2'), ('legislation', 'C1'), ('diplomacy', 'C1'), ('sovereignty', 'C2'), ('partisanship', 'C2')],
    'technology': [('computer', 'A1'), ('software', 'A2'), ('digital', 'B1'), ('innovation', 'B2'), ('internet', 'A2'), ('artificial intelligence', 'C1'), ('cybersecurity', 'C1'), ('quantum computing', 'C2'), ('blockchain', 'C2')],
    'education': [('learning', 'A2'), ('student', 'A1'), ('teacher', 'A1'), ('knowledge', 'B1'), ('classroom', 'A2'), ('curriculum', 'B2'), ('assessment', 'C1'), ('pedagogy', 'C2'), ('epistemology', 'C2')],
    'environment': [('nature', 'A2'), ('pollution', 'B1'), ('climate change', 'B2'), ('recycle', 'B1'), ('sustainability', 'C1'), ('ecosystem', 'B2'), ('deforestation', 'C1'), ('biodiversity', 'C2'), ('anthropogenic', 'C2')],
    'health': [('doctor', 'A1'), ('disease', 'B1'), ('treatment', 'B2'), ('nutrition', 'B2'), ('mental health', 'B2'), ('vaccine', 'C1'), ('epidemic', 'C1'), ('immunology', 'C2'), ('pathogenesis', 'C2')],
    'travel': [('airport', 'A1'), ('ticket', 'A1'), ('passport', 'A2'), ('tourism', 'B1'), ('adventure', 'B2'), ('itinerary', 'C1'), ('accommodation', 'B2'), ('expedition', 'C2'), ('cosmopolitan', 'C2')],
    'culture': [('tradition', 'A2'), ('festival', 'A2'), ('language', 'A1'), ('heritage', 'B2'), ('custom', 'B1'), ('ritual', 'C1'), ('diversity', 'B2'), ('ethnography', 'C2'), ('assimilation', 'C2')]
}

# Create a simple in-memory cache for word definitions
DEFINITIONS_CACHE = {}

# Common pre-defined definitions to avoid API calls for common words
COMMON_DEFINITIONS = {
    'company': {
        'definition': 'A business organization that makes or sells goods or services.',
        'example': 'She works for a large technology company.',
        'part_of_speech': 'noun',
        'synonyms': 'firm, business, corporation, enterprise',
        'pronunciation': 'ˈkʌmpəni',
        'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/company-us.mp3'
    },
    'computer': {
        'definition': 'An electronic device for storing and processing data according to instructions.',
        'example': 'She uses her computer for work and gaming.',
        'part_of_speech': 'noun',
        'synonyms': 'PC, laptop, workstation, machine',
        'pronunciation': 'kəmˈpjuːtə',
        'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/computer-us.mp3'
    },
    'student': {
        'definition': 'A person who is studying at a school or university.',
        'example': 'The student submitted her assignment on time.',
        'part_of_speech': 'noun',
        'synonyms': 'pupil, learner, scholar, undergraduate',
        'pronunciation': 'ˈstjuːdənt',
        'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/student-us.mp3'
    },
    'teacher': {
        'definition': 'A person who teaches, especially in a school.',
        'example': 'My favorite teacher taught mathematics.',
        'part_of_speech': 'noun',
        'synonyms': 'instructor, educator, tutor, professor',
        'pronunciation': 'ˈtiːtʃə',
        'audio': 'https://api.dictionaryapi.dev/media/pronunciations/en/teacher-us.mp3'
    },
}

def get_word_definition(word):
    """
    Enhanced function to fetch word definitions with additional fields:
    - part of speech
    - synonyms
    - pronunciation
    - audio
    """
    # Convert to lowercase for consistent lookup
    word_lower = word.lower()
    
    # Check if we already have this definition cached
    if word_lower in DEFINITIONS_CACHE:
        return DEFINITIONS_CACHE[word_lower]
    
    # Check if it's a common word with a pre-defined definition
    if word_lower in COMMON_DEFINITIONS:
        DEFINITIONS_CACHE[word_lower] = COMMON_DEFINITIONS[word_lower]
        return COMMON_DEFINITIONS[word_lower]
        
    # Otherwise, fetch from API with a timeout
    try:
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_lower}", 
            timeout=3  # 3-second timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                # Get all available information
                first_entry = data[0]
                meanings = first_entry.get('meanings', [])
                
                if meanings and len(meanings) > 0:
                    first_meaning = meanings[0]
                    definition = first_meaning.get('definitions', [{}])[0].get('definition', '')
                    example = first_meaning.get('definitions', [{}])[0].get('example', '')
                    part_of_speech = first_meaning.get('partOfSpeech', '')
                    
                    # Get synonyms
                    synonyms = []
                    for meaning in meanings:
                        if 'synonyms' in meaning:
                            synonyms.extend(meaning.get('synonyms', []))
                        for definition_obj in meaning.get('definitions', []):
                            if 'synonyms' in definition_obj:
                                synonyms.extend(definition_obj.get('synonyms', []))
                    
                    # Limit to 5 synonyms
                    synonyms = synonyms[:5]
                    synonyms_str = ", ".join(synonyms)
                    
                    # Get pronunciation
                    phonetics = first_entry.get('phonetics', [])
                    pronunciation = ""
                    audio_url = ""
                    
                    for phonetic in phonetics:
                        if phonetic.get('text'):
                            pronunciation = phonetic.get('text')
                        if phonetic.get('audio') and not audio_url:
                            audio_url = phonetic.get('audio')
                    
                    result = {
                        'definition': definition,
                        'example': example,
                        'part_of_speech': part_of_speech,
                        'synonyms': synonyms_str,
                        'pronunciation': pronunciation,
                        'audio': audio_url
                    }
                    
                    # Cache the result for future requests
                    DEFINITIONS_CACHE[word_lower] = result
                    return result
        
        # Fallback result if API fails
        fallback = {
            'definition': f"Definition for {word}",
            'example': f"Example sentence using the word {word}.",
            'part_of_speech': 'noun',  # Default to noun
            'synonyms': '',
            'pronunciation': '',
            'audio': ''
        }
        DEFINITIONS_CACHE[word_lower] = fallback
        return fallback
        
    except Exception as e:
        print(f"Error fetching definition for {word}: {str(e)}")
        fallback = {
            'definition': f"Definition for {word}",
            'example': f"Example sentence using the word {word}.",
            'part_of_speech': 'noun',  # Default to noun
            'synonyms': '',
            'pronunciation': '',
            'audio': ''
        }
        DEFINITIONS_CACHE[word_lower] = fallback
        return fallback

def vocabulary_list_view(request):
    """
    Display a list of vocabulary topics with word counts for each topic.
    """
    # Get selected difficulty level from query params, or default to 'all'
    difficulty_level = request.GET.get('level', 'all')
    
    # Get list of topics with counts
    topics = []
    
    for topic, word_list in TOPIC_WORDS.items():
        # Filter words by difficulty level if a specific level is selected
        if difficulty_level != 'all':
            filtered_words = [word for word, level in word_list if level == difficulty_level]
            count = len(filtered_words)
        else:
            count = len(word_list)
        
        # For each topic, also count words from the database
        if difficulty_level != 'all':
            db_count = Vocabulary.objects.filter(topic=topic, level=difficulty_level).count()
        else:
            db_count = Vocabulary.objects.filter(topic=topic).count()
        
        # Add to total count
        total_count = count + db_count
        
        if total_count > 0:
            topics.append({
                "topic": topic,
                "count": total_count,
                "display_name": topic.capitalize()
            })
    
    # Sort topics by name
    topics.sort(key=lambda x: x["topic"])
    
    # Available difficulty levels for filtering
    difficulty_levels = [
        {'code': 'all', 'name': 'All Levels'},
        {'code': 'A1', 'name': 'Beginner (A1)'},
        {'code': 'A2', 'name': 'Elementary (A2)'},
        {'code': 'B1', 'name': 'Intermediate (B1)'},
        {'code': 'B2', 'name': 'Upper Intermediate (B2)'},
        {'code': 'C1', 'name': 'Advanced (C1)'},
        {'code': 'C2', 'name': 'Proficiency (C2)'}
    ]
    
    # Context dictionary to pass to the template
    context = {
        'topics': topics,
        'title': 'Vocabulary By Topic',
        'difficulty_levels': difficulty_levels,
        'selected_level': difficulty_level
    }
    
    # Render the template with the context
    return render(request, 'vocabulary_list.html', context)

def vocabulary_topic_view(request, topic):
    """
    Display all vocabulary words for a specific topic with difficulty level filtering.
    
    Args:
        request: The HTTP request
        topic: The topic to filter vocabulary words by
    """
    # Get selected difficulty level from query params, or default to 'all'
    difficulty_level = request.GET.get('level', 'all')
    
    # For authenticated users, get their saved words to mark them as saved
    saved_words_set = set()
    if request.user.is_authenticated:
        saved_words = SavedWord.objects.filter(user=request.user).values_list('word', flat=True)
        saved_words_set = set(word.lower() for word in saved_words)
    
    # Get words from the database for this topic
    if difficulty_level != 'all':
        db_words = list(Vocabulary.objects.filter(topic=topic, level=difficulty_level))
    else:
        db_words = list(Vocabulary.objects.filter(topic=topic))
    
    # Convert database words to dictionary format
    formatted_db_words = []
    existing_words = set()  # Track existing words to avoid duplicates
    
    for word_obj in db_words:
        formatted_db_words.append({
            'word': word_obj.word,
            'definition': word_obj.definition,
            'example': getattr(word_obj, 'example', ''),
            'is_saved': word_obj.word.lower() in saved_words_set,
            'level': getattr(word_obj, 'level', 'B1'),  # Default to B1 if not specified
            'part_of_speech': getattr(word_obj, 'part_of_speech', ''),
            'synonyms': getattr(word_obj, 'synonyms', ''),
            'pronunciation': getattr(word_obj, 'pronunciation', ''),
            'audio': getattr(word_obj, 'audio', None),
            # Additional fields for flashcards
            'front': word_obj.word,
            'back': word_obj.definition
        })
        existing_words.add(word_obj.word.lower())
    
    # Get sample words for this topic from our predefined list
    sample_words = []
    
    if topic in TOPIC_WORDS:
        # Get words for this topic
        topic_word_list = TOPIC_WORDS[topic]
        
        # Filter words by difficulty level if needed
        if difficulty_level != 'all':
            filtered_words = [(word, level) for word, level in topic_word_list if level == difficulty_level]
        else:
            filtered_words = topic_word_list
        
        # Only fetch sample words that don't already exist in the database
        words_to_fetch = [word for word, _ in filtered_words if word.lower() not in existing_words]
        
        # Limit the number of words to fetch
        max_words_to_fetch = 10
        
        for word in words_to_fetch[:max_words_to_fetch]:
            # Get detailed word information
            word_info = get_word_definition(word)
            
            # Find the level for this word
            word_level = next((level for w, level in topic_word_list if w.lower() == word.lower()), 'B1')
            
            sample_words.append({
                'word': word,
                'definition': word_info['definition'],
                'example': word_info['example'],
                'is_saved': word.lower() in saved_words_set,
                'level': word_level,
                'part_of_speech': word_info['part_of_speech'],
                'synonyms': word_info['synonyms'],
                'pronunciation': word_info['pronunciation'],
                'audio': word_info['audio'],
                # Additional fields for flashcards
                'front': word,
                'back': word_info['definition']
            })
    
    # Combine database words with sample words
    all_words = formatted_db_words + sample_words
    
    # Available difficulty levels for filtering
    difficulty_levels = [
        {'code': 'all', 'name': 'All Levels'},
        {'code': 'A1', 'name': 'Beginner (A1)'},
        {'code': 'A2', 'name': 'Elementary (A2)'},
        {'code': 'B1', 'name': 'Intermediate (B1)'},
        {'code': 'B2', 'name': 'Upper Intermediate (B2)'},
        {'code': 'C1', 'name': 'Advanced (C1)'},
        {'code': 'C2', 'name': 'Proficiency (C2)'}
    ]
    
    # Context dictionary to pass to the template
    context = {
        'words': all_words,
        'topic': topic.capitalize(),
        'title': f'Vocabulary: {topic.capitalize()}',
        'difficulty_levels': difficulty_levels,
        'selected_level': difficulty_level,
        'flashcards_enabled': True,  # Enable flashcard view
        # Change this in vocabulary_topic_view function:
        'flashcards': json.dumps([
            {
                'id': index,
                'front': word['word'],
                'back': word['definition'],
                'level': word['level'],
                'part_of_speech': word['part_of_speech'],
                'pronunciation': word['pronunciation'],
                'example': word['example'],
                'synonyms': word['synonyms'],
                'audio': word['audio'],
                'is_saved': word['is_saved']
            }
            for index, word in enumerate(all_words)
        ])
    }
    
    # Render the template with the context
    return render(request, 'vocabulary_topic.html', context)

@login_required
def save_favorite_word(request):
    """
    Save a favorite vocabulary word for an authenticated user.
    
    This enhanced version stores additional fields:
    - topic
    - level
    - part_of_speech
    - synonyms
    - pronunciation
    - audio
    
    Returns:
        JsonResponse: Success or error message
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        word = data.get('word')
        definition = data.get('definition')
        example = data.get('example', '')
        
        # New fields
        topic = data.get('topic', '')
        level = data.get('level', 'B1')  # Default to intermediate
        part_of_speech = data.get('part_of_speech', '')
        synonyms = data.get('synonyms', '')
        pronunciation = data.get('pronunciation', '')
        audio = data.get('audio', '')
        
        # Validate required fields
        if not word or not definition:
            return JsonResponse({'error': 'Word and definition are required'}, status=400)
        
        # Check if the word already exists for this user
        existing_word = FavoriteVocabulary.objects.filter(
            user=request.user,
            word=word
        ).first()
        
        if existing_word:
            # Update the existing word
            existing_word.definition = definition
            existing_word.example = example
            
            # Update new fields
            if topic:
                existing_word.topic = topic
            if level:
                existing_word.level = level
            if part_of_speech:
                existing_word.part_of_speech = part_of_speech
            if synonyms:
                existing_word.synonyms = synonyms
            if pronunciation:
                existing_word.pronunciation = pronunciation
            if audio:
                existing_word.audio = audio
                
            existing_word.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Updated "{word}" in your favorites',
                'id': existing_word.id
            })
        else:
            # Create a new favorite word for the authenticated user
            favorite = FavoriteVocabulary.objects.create(
                user=request.user,
                word=word,
                definition=definition,
                example=example,
                topic=topic,
                level=level,
                part_of_speech=part_of_speech,
                synonyms=synonyms,
                pronunciation=pronunciation,
                audio=audio
            )
            
            return JsonResponse({
                'success': True,
                'message': f'"{word}" has been added to your favorites',
                'id': favorite.id
            })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def favorites_view(request):
    """
    Display a list of favorite vocabulary words for the authenticated user.
    
    Enhanced to support filtering by topic and difficulty level.
    """
    # Get filter parameters
    topic_filter = request.GET.get('topic', '')
    level_filter = request.GET.get('level', '')
    
    # Base query
    query = FavoriteVocabulary.objects.filter(user=request.user)
    
    # Apply filters
    if topic_filter:
        query = query.filter(topic=topic_filter)
    
    if level_filter:
        query = query.filter(level=level_filter)
    
    # Get results
    favorites = query.order_by('word')
    
    # Get topics for filter dropdown
    topics = FavoriteVocabulary.objects.filter(user=request.user).values('topic').distinct()
    topics = [topic['topic'] for topic in topics if topic['topic']]
    
    # Difficulty levels for filter dropdown
    difficulty_levels = [
        {'code': 'A1', 'name': 'Beginner (A1)'},
        {'code': 'A2', 'name': 'Elementary (A2)'},
        {'code': 'B1', 'name': 'Intermediate (B1)'},
        {'code': 'B2', 'name': 'Upper Intermediate (B2)'},
        {'code': 'C1', 'name': 'Advanced (C1)'},
        {'code': 'C2', 'name': 'Proficiency (C2)'}
    ]
    
    # Context dictionary to pass to the template
    context = {
        'favorites': favorites,
        'title': 'My Favorite Words',
        'total_count': favorites.count(),
        'topics': topics,
        'difficulty_levels': difficulty_levels,
        'selected_topic': topic_filter,
        'selected_level': level_filter,
        'flashcards_enabled': True,
        'flashcards': json.dumps([
            {
                'id': word.id,
                'front': word.word,
                'back': word.definition,
                'level': word.level or 'B1'
            }
            for word in favorites
        ])
    }
    
    # Render the template with the context
    return render(request, 'favorites.html', context)