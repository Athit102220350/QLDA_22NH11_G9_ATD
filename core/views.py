from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    """View for the homepage."""
    return render(request, 'index.html')

def chatbot(request):
    """View for the chatbot page."""
    return render(request, 'chatbot.html')

@csrf_exempt
def process_message(request):
    """Handle chatbot API interaction."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Here we would normally call an external AI API
            # For demonstration, we're using a simple grammar correction logic
            
            grammar_mistakes = {
                "i goed": "I went",
                "i has": "I have",
                "i is": "I am",
                "they is": "they are",
                "she have": "she has",
                "he have": "he has",
                "we was": "we were",
                "they was": "they were"
            }
            
            response_message = user_message
            for mistake, correction in grammar_mistakes.items():
                if mistake in user_message.lower():
                    response_message = f"Correction: {user_message.lower().replace(mistake, correction)}"
                    break
            else:
                # If no grammar mistakes found
                response_message = "Your English looks good!"
                
            return JsonResponse({'response': response_message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
