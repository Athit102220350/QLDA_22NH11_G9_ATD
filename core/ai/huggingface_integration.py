"""
Hugging Face Grammar and Vocabulary Assistance Module
"""
import os
import requests
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Load environment variables from .env file
load_dotenv()

class GrammarCorrector:
    """Class to handle grammar correction using Hugging Face models"""
    
    def __init__(self):
        """Initialize the grammar corrector with pre-trained models"""
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # Load the T5 grammar correction model
        try:
            self.model_name = "prithivida/grammar_error_correcter_v1"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.grammar_corrector = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=128
            )
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading local model: {e}")
            self.model_loaded = False
    
    
    def correct_grammar(self, text):
        """
        Correct grammar in the provided text
        Args:
            text (str): Text to correct
        Returns:
            str: Corrected text and explanation
        """
        if not text:
            return "Please provide some text."
        
        # Try using the local model first
        if self.model_loaded:
            try:
                # Prefix required by the grammar correction model
                input_text = f"grammar: {text}"
                corrected = self.grammar_corrector(input_text, max_length=128)[0]['generated_text']
                
                if corrected.lower() == text.lower():
                    return {
                        "corrected_text": corrected,
                        "has_errors": False,
                        "explanation": "No grammar errors found."
                    }
                else:
                    return {
                        "corrected_text": corrected,
                        "has_errors": True,
                        "explanation": self._generate_explanation(text, corrected)
                    }
            except Exception as e:
                print(f"Local model error: {e}")
                # Fall back to API if local model fails
                pass
        
        # Fallback to the API
        if self.api_key:
            return self._use_api_for_correction(text)
        else:
            # Simple fallback if no model or API is available
            return {
                "corrected_text": text,
                "has_errors": False,
                "explanation": "Grammar checking unavailable. Please check your configuration."
            }
    
    def _use_api_for_correction(self, text):
        """Use the Hugging Face API to correct grammar"""
        API_URL = f"https://api-inference.huggingface.co/models/prithivida/grammar_error_correcter_v1"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            payload = {"inputs": f"grammar: {text}"}
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                corrected = result[0].get('generated_text', text)
                
                if corrected.lower() == text.lower():
                    return {
                        "corrected_text": corrected,
                        "has_errors": False,
                        "explanation": "No grammar errors found."
                    }
                else:
                    return {
                        "corrected_text": corrected,
                        "has_errors": True,
                        "explanation": self._generate_explanation(text, corrected)
                    }
            else:
                return {
                    "corrected_text": text,
                    "has_errors": False,
                    "explanation": "Could not analyze grammar. Please try again."
                }
        
        except Exception as e:
            print(f"API error: {e}")
            return {
                "corrected_text": text,
                "has_errors": False,
                "explanation": "Error connecting to grammar service."
            }
    
    def _generate_explanation(self, original, corrected):
        """Generate an explanation of what was corrected"""
        # Simple diff-based explanation
        if original.lower() == corrected.lower():
            return "No grammar errors found."
        
        # Split into words for comparison
        original_words = original.split()
        corrected_words = corrected.split()
        
        # Find differences (very simplified)
        explanation = []
        
        if len(original_words) != len(corrected_words):
            # If word count is different, just give a general explanation
            explanation.append(f"Your sentence structure needed adjustment.")
        else:
            # Check word by word
            for i, (orig, corr) in enumerate(zip(original_words, corrected_words)):
                if orig.lower() != corr.lower():
                    explanation.append(f"'{orig}' was corrected to '{corr}'.")
        
        if not explanation:
            explanation.append("Grammar was improved.")
            
        return " ".join(explanation)


class VocabularyEnhancer:
    """Class to provide vocabulary assistance using Hugging Face models"""
    
    def __init__(self):
        """Initialize the vocabulary enhancer"""
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # Load a word definition model
        try:
            self.definition_model_name = "sentence-transformers/all-MiniLM-L6-v2"
            self.definition_tokenizer = AutoTokenizer.from_pretrained(self.definition_model_name)
            self.definition_pipeline = pipeline(
                "feature-extraction",
                model=self.definition_model_name,
                tokenizer=self.definition_tokenizer
            )
            self.model_loaded = True
            
            # Dictionary of common words with definitions and examples
            self.word_database = {
                "ameliorate": {
                    "definition": "make (something bad or unsatisfactory) better.",
                    "example": "The medicine ameliorated the patient's condition.",
                    "synonyms": ["improve", "better", "enhance"]
                },
                "ephemeral": {
                    "definition": "lasting for a very short time.",
                    "example": "The ephemeral nature of fashion trends makes them difficult to follow.",
                    "synonyms": ["transitory", "fleeting", "brief"]
                },
                "ubiquitous": {
                    "definition": "present, appearing, or found everywhere.",
                    "example": "Mobile phones have become ubiquitous in modern society.",
                    "synonyms": ["omnipresent", "ever-present", "pervasive"]
                },
                "pragmatic": {
                    "definition": "dealing with things sensibly and realistically.",
                    "example": "We need a pragmatic approach to solving this problem.",
                    "synonyms": ["practical", "realistic", "sensible"]
                },
                "diligent": {
                    "definition": "having or showing care and conscientiousness in one's work or duties.",
                    "example": "She was a diligent student who always completed her homework.",
                    "synonyms": ["hardworking", "industrious", "assiduous"]
                }
            }
        except Exception as e:
            print(f"Error loading vocabulary model: {e}")
            self.model_loaded = False

    def get_word_info(self, word):
        """
        Get information about a word including definition, examples, and synonyms
        Args:
            word (str): Word to lookup
        Returns:
            dict: Word information
        """
        if not word:
            return {"error": "Please provide a word."}
        
        # Clean the word
        word = word.lower().strip()
        
        # Check our local database first
        if word in self.word_database:
            return {
                "word": word,
                "definition": self.word_database[word]["definition"],
                "example": self.word_database[word]["example"],
                "synonyms": self.word_database[word]["synonyms"]
            }
        
        # Use the API as fallback
        if self.api_key:
            return self._use_api_for_word_info(word)
        
        return {
            "word": word,
            "error": "Word information not available."
        }
    
    def _use_api_for_word_info(self, word):
        """Use the Hugging Face API to get word information"""
        # This would be replaced with a real dictionary API
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            # Generate a definition-like response
            payload = {"inputs": f"Define the word '{word}':"}
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                definition = result[0].get('generated_text', '')
                
                return {
                    "word": word,
                    "definition": definition,
                    "example": "No example available.",
                    "synonyms": []
                }
            else:
                return {
                    "word": word,
                    "error": "Could not find information for this word."
                }
                
        except Exception as e:
            print(f"API error: {e}")
            return {
                "word": word,
                "error": "Error connecting to vocabulary service."
            }
    
    def suggest_alternative_words(self, word, context=""):
        """
        Suggest alternative (better) words based on context
        Args:
            word (str): Word to find alternatives for
            context (str): Optional context where the word is used
        Returns:
            list: Alternative words
        """
        # This is a simplified version - in a real application, 
        # you'd use a more sophisticated approach with word embeddings
        
        common_replacements = {
            "good": ["excellent", "outstanding", "superb", "exceptional"],
            "bad": ["poor", "inadequate", "substandard", "deficient"],
            "happy": ["delighted", "elated", "joyful", "ecstatic"],
            "sad": ["unhappy", "melancholy", "despondent", "gloomy"],
            "big": ["large", "substantial", "enormous", "massive"],
            "small": ["tiny", "diminutive", "miniature", "compact"],
            "pretty": ["attractive", "beautiful", "gorgeous", "lovely"],
            "ugly": ["unattractive", "unsightly", "hideous", "grotesque"]
        }
        
        word = word.lower().strip()
        
        if word in common_replacements:
            return {
                "word": word,
                "alternatives": common_replacements[word]
            }
        
        # If we have the API key, we could use a model for this
        if self.api_key and context:
            return self._use_api_for_alternatives(word, context)
        
        return {
            "word": word,
            "alternatives": []
        }
    
    def _use_api_for_alternatives(self, word, context):
        """Use the Hugging Face API to suggest alternative words"""
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            payload = {
                "inputs": f"Replace the word '{word}' with better alternatives in this context: {context}"
            }
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                suggestions_text = result[0].get('generated_text', '')
                # Extract words from the response - this would need to be improved
                alternatives = [
                    w.strip('.,;:"\'()[]{}') 
                    for w in suggestions_text.split() 
                    if w.strip('.,;:"\'()[]{}').lower() != word.lower()
                ][:5]  # Limit to 5 alternatives
                
                return {
                    "word": word,
                    "alternatives": alternatives
                }
            else:
                return {
                    "word": word,
                    "alternatives": []
                }
                
        except Exception as e:
            print(f"API error: {e}")
            return {
                "word": word,
                "alternatives": []
            }
    
    # Add these functions to the VocabularyEnhancer class after the existing methods

    def lookup_vocabulary(self, word):
        """
        Enhanced vocabulary lookup using dictionary API and Hugging Face models
        Args:
            word (str): Word to lookup
        Returns:
            dict: Word information with definition, example, and synonyms
        """
        if not word:
            return {"error": "Please provide a word."}
        
        # Clean the word
        word = word.lower().strip()
        
        # Check our local database first
        if word in self.word_database:
            return {
                "word": word,
                "definition": self.word_database[word]["definition"],
                "example": self.word_database[word]["example"],
                "synonyms": self.word_database[word]["synonyms"]
            }
        
        # Use external dictionary API
        try:
            api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Extract definition
                    meanings = data[0].get('meanings', [])
                    definition = "Definition not available"
                    example = "Example not available"
                    synonyms = []
                    
                    if meanings:
                        # Get the first definition
                        definition = meanings[0].get('definitions', [{}])[0].get('definition', definition)
                        
                        # Get the first example
                        example = meanings[0].get('definitions', [{}])[0].get('example', example)
                        
                        # Collect synonyms from all meanings
                        for meaning in meanings:
                            for def_item in meaning.get('definitions', []):
                                syns = def_item.get('synonyms', [])
                                if syns:
                                    synonyms.extend(syns[:3])  # Limit to 3 synonyms per definition
                        
                        # Remove duplicates and limit total
                        synonyms = list(dict.fromkeys(synonyms))[:10]
                    
                    return {
                        "word": word,
                        "definition": definition,
                        "example": example,
                        "synonyms": synonyms
                    }
        except Exception as e:
            print(f"Dictionary API error: {e}")
        
        # Fallback to Hugging Face API
        if self.api_key:
            return self._use_api_for_word_info(word)
        
        return {
            "word": word,
            "error": "Word information not available."
        }

    def find_word_alternatives(self, word, context=""):
        """
        Find contextually appropriate word alternatives using Hugging Face models
        Args:
            word (str): Word to find alternatives for
            context (str): Context where the word is used
        Returns:
            dict: Word and list of alternative words
        """
        if not word:
            return {"error": "Please provide a word."}
        
        word = word.lower().strip()
        alternatives = []
        
        # Check our local database first
        if word in self.word_database and "synonyms" in self.word_database[word]:
            alternatives = self.word_database[word]["synonyms"]
        
        # Use hardcoded common replacements if available
        common_replacements = {
            "good": ["excellent", "outstanding", "superb", "exceptional"],
            "bad": ["poor", "inadequate", "substandard", "deficient"],
            "happy": ["delighted", "elated", "joyful", "ecstatic"],
            "sad": ["unhappy", "melancholy", "despondent", "gloomy"],
            "big": ["large", "substantial", "enormous", "massive"],
            "small": ["tiny", "diminutive", "miniature", "compact"],
            "pretty": ["attractive", "beautiful", "gorgeous", "lovely"],
            "ugly": ["unattractive", "unsightly", "hideous", "grotesque"]
        }
        
        if word in common_replacements:
            alternatives = common_replacements[word]
        
        # If context is provided, use a mask-filling approach with BERT
        if context and self.api_key:
            context_alternatives = self._get_masked_alternatives(word, context)
            
            # Combine results, prioritizing context-aware alternatives
            if context_alternatives:
                # Add context alternatives at the beginning, avoiding duplicates
                for alt in reversed(context_alternatives):
                    if alt.lower() != word.lower() and alt not in alternatives:
                        alternatives.insert(0, alt)
        
        return {
            "word": word,
            "context": context,
            "alternatives": alternatives[:10]  # Limit to top 10 alternatives
        }

    def _get_masked_alternatives(self, word, context):
        """Use BERT mask-filling to get contextual word alternatives"""
        # Replace word with [MASK] in context
        masked_context = context.replace(word, "[MASK]")
        
        # If word wasn't found in context, try a simple approach
        if "[MASK]" not in masked_context:
            words = context.split()
            for i, w in enumerate(words):
                if w.lower() == word.lower():
                    words[i] = "[MASK]"
                    masked_context = " ".join(words)
                    break
        
        # If still no mask, create a simple masked sentence
        if "[MASK]" not in masked_context:
            masked_context = f"The [MASK] {context}"
        
        API_URL = "https://api-inference.huggingface.co/models/bert-base-uncased"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            payload = {"inputs": masked_context}
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()
            
            alternatives = []
            if isinstance(result, list):
                for item in result:
                    # Extract the predictions for the masked token
                    if isinstance(item, list):
                        for prediction in item:
                            if isinstance(prediction, dict) and 'token_str' in prediction:
                                token = prediction['token_str'].strip()
                                if token.lower() != word.lower() and len(token) > 1:
                                    alternatives.append(token)
            
            return alternatives[:5]  # Return top 5 alternatives
            
        except Exception as e:
            print(f"BERT API error: {e}")
            return []


# Create instances to use
grammar_corrector = GrammarCorrector()
vocabulary_enhancer = VocabularyEnhancer()
