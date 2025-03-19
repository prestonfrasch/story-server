import chainlit as cl
import requests
import json
from typing import List, Tuple
from cast_of_characters import characters, Character
from story import story_opening
# Student can add NLTK imports here
# import nltk
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize conversation context and characters
conversation_context: List[str] = []

# Constants 
LMSTUDIO_API_URL = "http://localhost:1234/v1/completions"
MAX_CONTEXT_MESSAGES = 10
MAX_TOKENS = 4096

def get_character_from_message(message: str) -> Tuple[Character, str]:
    """Extract character mention and clean message"""
    for char_name in characters.keys():
        if f"@{char_name}" in message.lower():
            return characters[char_name], message.replace(f"@{char_name}", "").strip()
    return characters["narrator"], message.strip()

def analyze_user_message(message: str) -> str:
    """
    STUDENT EXERCISE OPPORTUNITY:
    Analyze user message before processing
    Ideas:
    - Check sentiment of user message
    - Count words/sentences
    - Identify key topics or entities
    - Tag parts of speech
    """
    return message

def analyze_generated_text(text: str) -> str:
    """
    STUDENT EXERCISE OPPORTUNITY:
    Analyze generated text before processing
    Ideas:
    - Check sentiment of generated text
    - Count words/sentences
    - Identify key topics or entities
    - Tag parts of speech
    """
    return text

def process_generated_text(text: str) -> str:
    """
    STUDENT EXERCISE OPPORTUNITY:
    Process the LLM generated text before display
    Ideas:
    - Add paragraph breaks after N sentences
    - Convert negative sentiment to positive
    - Add emphasis to key words
    - Format dialogue with quotes
    - Replace words with synonyms
    """
    return text

@cl.on_chat_start
async def start():
    """Initialize chat with story opening"""
    msg = cl.Message(content=story_opening)
    await msg.send()
    conversation_context.append(f"Narrator: {story_opening}")

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    try:
        # 1. Analyze user message (STUDENT CODE CAN BE USED HERE WITH THIS FUNCTION)
        analyzed_message = analyze_user_message(message.content)
        
        # 2. Get character and clean message
        character, clean_message = get_character_from_message(analyzed_message)
        
        # 3. Add user message to context
        conversation_context.append(f"User: {clean_message}")
        
        # 4. Construct full prompt with system prompt and conversation history
        full_prompt = f"""System Prompt: {character.role}

Conversation History:
{chr(10).join(conversation_context[-MAX_CONTEXT_MESSAGES:])}

{character.name}:"""

        # Prepare API payload
        payload = {
            "model": "mistral-7b-instruct-v0.3",
            "prompt": full_prompt,
            "temperature": 0.7,
            "stream": True,
            "max_tokens": 1024
        }

        # Send request to LM Studio's API
        msg.content = f"@{character.name} "
        await msg.update()
        
        response = requests.post(LMSTUDIO_API_URL, json=payload, stream=True)
        response.raise_for_status()

        accumulated_response = ""
        
        # Process streaming response
        first_token = True  # Track if it's the first token
        for line in response.iter_lines():
            if line:
                try:
                    clean_line = line.decode("utf-8").strip()
                    if clean_line.startswith("data: "):
                        clean_line = clean_line[6:].strip()
                    
                    if clean_line == "[DONE]":
                        break

                    decoded_line = json.loads(clean_line)
                    text_part = decoded_line.get("choices", [{}])[0].get("text", "")

                    if "User" in text_part:
                        break

                    if text_part:
                        # Option to Process text tokens in real-time
                        # STUDENT EXERCISE: Add token-level processing here
                        accumulated_response += text_part
                        await msg.stream_token(text_part)

                except json.JSONDecodeError:
                    continue

        # Process complete response
        if accumulated_response.strip():
            
            

            # STUDENT EXERCISE OPTION: Further analyze response characteristics
            # Example analyses:
            # - Count words/sentences
            # - Measure sentiment
            # - Extract key phrases
            # - Identify named entities
            analyzed_message = analyze_generated_text(accumulated_response.strip())
            # STUDENT EXERCISE: Process full response
            processed_response = process_generated_text(analyzed_message)
            

            conversation_context.append(f"{character.name}: {processed_response}")
            await msg.send()
        else:
            await cl.Message(content="Sorry, I couldn't generate a response.").send()

    except requests.RequestException as e:
        error_msg = f"Error communicating with LM Studio: {str(e)}"
        print(error_msg)
        await cl.Message(content=error_msg).send()
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)
        await cl.Message(content=error_msg).send()
