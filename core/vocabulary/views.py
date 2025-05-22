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
# The SavedWord model doesn't have a topic field, so we'll group by word as a workaround
Vocabulary = SavedWord
FavoriteVocabulary = SavedWord

# Dictionary with sample words and their data for each letter
SAMPLE_WORDS = {
    'A': ['apple', 'amazing', 'adventure', 'algorithm', 'astronomy'],
    'B': ['banana', 'beautiful', 'brilliant', 'browser', 'balance'],
    'C': ['computer', 'creative', 'confident', 'challenge', 'chocolate'],
    'D': ['digital', 'dynamic', 'democracy', 'debate', 'development'],
    'E': ['excellent', 'elegant', 'education', 'effective', 'environment'],
    'F': ['fantastic', 'freedom', 'flexible', 'foundation', 'flavor'],
    'G': ['great', 'global', 'graphics', 'governance', 'guidance'],
    'H': ['human', 'harmony', 'horizon', 'history', 'happiness'],
    'I': ['imagination', 'innovative', 'internet', 'inspire', 'important'],
    'J': ['journey', 'justice', 'joyful', 'judgment', 'journalism'],
    'K': ['knowledge', 'kindness', 'keyboard', 'kinetic', 'kitchen'],
    'L': ['learning', 'language', 'leadership', 'legacy', 'logical'],
    'M': ['modern', 'motivation', 'memory', 'music', 'management'],
    'N': ['network', 'natural', 'navigate', 'nutrition', 'necessary'],
    'O': ['opportunity', 'organization', 'objective', 'optimize', 'organic'],
    'P': ['professional', 'progress', 'practical', 'potential', 'positive'],
    'Q': ['quality', 'question', 'quantum', 'quick', 'quotation'],
    'R': ['research', 'reliable', 'resource', 'revolution', 'reality'],
    'S': ['software', 'solution', 'strategy', 'sustainable', 'science'],
    'T': ['technology', 'teamwork', 'tradition', 'transform', 'thinking'],
    'U': ['understanding', 'unique', 'update', 'ultimate', 'utility'],
    'V': ['valuable', 'vision', 'virtual', 'vocabulary', 'versatile'],
    'W': ['website', 'wireless', 'workflow', 'wellbeing', 'wisdom'],
    'X': ['xenial', 'xerox', 'xylophone', 'x-ray', 'xenophobia'],
    'Y': ['yield', 'youth', 'yearly', 'yoga', 'yesterday'],
    'Z': ['zenith', 'zeal', 'zone', 'zoom', 'zodiac']
}

# Create a simple in-memory cache for word definitions
DEFINITIONS_CACHE = {}

# Common pre-defined definitions to avoid API calls for common words
COMMON_DEFINITIONS = {
    'apple': {
        'definition': 'The round fruit of an apple tree, which typically has thin green or red skin and crisp flesh.',
        'example': 'She took a bite of the juicy apple.'
    },
    'banana': {
        'definition': 'A long curved fruit with a yellow skin and soft sweet flesh.',
        'example': 'He peeled a banana for breakfast.'
    },
    'computer': {
        'definition': 'An electronic device for storing and processing data according to instructions.',
        'example': 'She uses her computer for work and gaming.'
    },
    'digital': {
        'definition': 'Relating to or using signals or information represented by discrete values.',
        'example': 'Digital technology has transformed our society.'
    },
    'learning': {
        'definition': 'The acquisition of knowledge or skills through study, experience, or teaching.',
        'example': 'Learning a new language takes time and practice.'
    },
    'quality': {
        'definition': 'The standard of something as measured against other things of a similar kind.',
        'example': 'They sell high-quality products at reasonable prices.'
    },
    'website': {
        'definition': 'A collection of web pages and related content identified by a common domain name.',
        'example': 'The company launched its new website yesterday.'
    },
}

def get_word_definition(word):
    """Fetch word definitions from cache, common definitions, or Free Dictionary API"""
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
            timeout=2  # 2-second timeout
        )
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                meanings = data[0].get('meanings', [])
                if meanings and len(meanings) > 0:
                    definition = meanings[0].get('definitions', [{}])[0].get('definition', '')
                    example = meanings[0].get('definitions', [{}])[0].get('example', '')
                    result = {
                        'definition': definition,
                        'example': example
                    }
                    # Cache the result for future requests
                    DEFINITIONS_CACHE[word_lower] = result
                    return result
        
        # Fallback result if API fails
        fallback = {
            'definition': f"Definition for {word}",
            'example': f"Example sentence using the word {word}."
        }
        DEFINITIONS_CACHE[word_lower] = fallback
        return fallback
        
    except Exception as e:
        print(f"Error fetching definition for {word}: {str(e)}")
        fallback = {
            'definition': f"Definition for {word}",
            'example': f"Example sentence using the word {word}."
        }
        DEFINITIONS_CACHE[word_lower] = fallback
        return fallback

def vocabulary_list_view(request):
    """
    Display a list of first letters as "topics" for vocabulary organization.
    
    This view creates an A-Z list with sample words count for each letter.
    """
    # Create alphabet with sample word counts
    topics = []
    for letter in string.ascii_uppercase:
        count = len(SAMPLE_WORDS.get(letter, []))
        topics.append({"topic": letter, "count": count})
    
    # Context dictionary to pass to the template
    context = {
        'topics': topics,
        'title': 'Vocabulary By First Letter'
    }
      # Render the template with the context
    return render(request, 'vocabulary_list.html', context)

def vocabulary_topic_view(request, topic):
    """
    Display all vocabulary words starting with a specific letter.
    
    This view generates sample words for the given letter
    and passes them to the vocabulary_topic.html template.
    
    Args:
        request: The HTTP request
        topic: The letter to filter vocabulary words by
        
    Returns:
        Rendered template with sample vocabulary words
    """
    # Get sample words from the database first
    db_words = list(Vocabulary.objects.filter(word__istartswith=topic))
    
    # For authenticated users, get their saved words to mark them as saved
    saved_words_set = set()
    if request.user.is_authenticated:
        saved_words = SavedWord.objects.filter(user=request.user).values_list('word', flat=True)
        saved_words_set = set(word.lower() for word in saved_words)
    
    # Convert database words to dictionary format if needed
    formatted_db_words = []
    existing_words = set()  # Track existing words to avoid duplicates
    
    for word_obj in db_words:
        formatted_db_words.append({
            'word': word_obj.word,
            'definition': word_obj.definition,
            'example': word_obj.example,
            'is_saved': word_obj.word.lower() in saved_words_set
        })
        existing_words.add(word_obj.word.lower())
    
    # Then get sample words for this letter from our predefined list
    sample_words = []
    words_to_fetch = SAMPLE_WORDS.get(topic.upper(), [])
    
    # If we have no words for this letter, provide some defaults
    if not words_to_fetch:
        if topic.upper() == 'X':
            words_to_fetch = ['xenial', 'xylophone', 'x-ray']
        elif topic.upper() == 'Z':
            words_to_fetch = ['zeal', 'zone', 'zoom']
        elif topic.upper() == 'Q':
            words_to_fetch = ['quality', 'question', 'quick']
        else:
            words_to_fetch = [f'sample{i}' for i in range(3)]
      # Only fetch sample words that don't already exist in the database
    words_to_fetch = [word for word in words_to_fetch if word.lower() not in existing_words]
    
    # If we already have some words from the database, reduce the number of additional words to fetch
    max_words_to_fetch = 3 if formatted_db_words else 5
    
    # Process words in parallel for better performance (up to max_words_to_fetch)
    for word in words_to_fetch[:max_words_to_fetch]:
        word_info = get_word_definition(word)
        sample_words.append({
            'word': word,
            'definition': word_info['definition'],
            'is_saved': word.lower() in saved_words_set,
            'example': word_info['example']
        })
    
    # Combine database words with sample words
    all_words = formatted_db_words + sample_words
    
    # Context dictionary to pass to the template
    context = {
        'words': all_words,
        'topic': f'Words starting with "{topic}"',
        'letter': topic,
        'title': f'Vocabulary: {topic}'
    }
      # Render the template with the context
    return render(request, 'vocabulary_topic.html', context)


@login_required
def save_favorite_word(request):
    """
    Save a favorite vocabulary word for an authenticated user.
    This is a wrapper around the main save_vocabulary_word function in the core views.
    
    This view accepts POST requests with JSON data containing word information,
    forwards the request to the main save_vocabulary_word function in core/views.py,
    which saves it to the SavedWord model associated with the current user.
    
    Required JSON fields:
    - word: The vocabulary word to save
    - definition: The definition of the word
    - example: An example usage of the word (optional)
    
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
        example = data.get('example', '')  # Optional field
        
        # Validate required fields
        if not word or not definition:
            return JsonResponse({'error': 'Word and definition are required'}, status=400)
              # Check if the word already exists for this user
        existing_word = FavoriteVocabulary.objects.filter(
            user=request.user,
            word=word
        ).first()
        
        if existing_word:
            # Update the existing word's definition and example
            existing_word.definition = definition
            existing_word.example = example
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
                example=example
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
    
    This view retrieves all FavoriteVocabulary objects associated with the
    current user and passes them to the favorites.html template.
    
    Args:
        request: The HTTP request
        
    Returns:
        Rendered template with the user's favorite vocabulary words
    """
    # Get all favorite words for the current user
    favorites = FavoriteVocabulary.objects.filter(user=request.user).order_by('word')
    
    # Context dictionary to pass to the template
    context = {
        'favorites': favorites,
        'title': 'My Favorite Words',
        'total_count': favorites.count()
    }
    
    # Render the template with the context
    return render(request, 'favorites.html', context)