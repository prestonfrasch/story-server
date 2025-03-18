import chainlit as cl
import requests
import json
import random
from typing import List, Tuple
from cast_of_characters import characters, Character

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

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    try:
        # Determine speaking character and clean message
        character, clean_message = get_character_from_message(message.content)
        
        # Add user message to context
        conversation_context.append(f"User: {clean_message}")
        
        # Construct full prompt with system prompt and history
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
        for line in response.iter_lines():
            if line:
                try:
                    clean_line = line.decode("utf-8").strip()
                    if clean_line.startswith("data: "):
                        clean_line = clean_line[6:].strip()
                    
                    if clean_line == "[DONE]":
                        break

                    decoded_line = json.loads(clean_line)
                    text_part = decoded_line.get("choices", [{}])[0].get("text", "").strip()

                    if "User" in text_part:
                        break

                    if text_part:
                        if accumulated_response and not accumulated_response.endswith(" "):
                            accumulated_response += " "
                        accumulated_response += text_part
                        await msg.stream_token(text_part + " ")

                except json.JSONDecodeError:
                    continue

        # Add AI response to context
        if accumulated_response.strip():
            conversation_context.append(f"{character.name}: {accumulated_response.strip()}")
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
