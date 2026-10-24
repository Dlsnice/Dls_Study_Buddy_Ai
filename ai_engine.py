"""
ai_engine.py
============
The core AI engine module.
Demonstrates how to connect to Google's Gemini models using modern best practices,
including system instructions, temperature control, and structured outputs.

Includes an automatic fallback (Demo Mode) so the app works even before you get an API key!
"""

import json
import os
from typing import List, Dict, Any, Optional

# Try importing the official Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# Model aliases to prevent 404 errors from deprecated model versions
MODEL_ALIASES = {
    "gemini-2.0-flash": "gemini-3.8-flash",
    "gemini-1.5-flash": "gemini-3.8-flash",
    "gemini-1.5-pro": "gemini-3.8-pro",
    "gemini-2.0-pro": "gemini-3.8-pro",
}

def _resolve_model(model_name: str) -> str:
    cleaned = model_name.replace("models/", "")
    return MODEL_ALIASES.get(cleaned, cleaned)


# ==============================================================================
# 1. CORE CHAT GENERATION
# ==============================================================================
def chat_with_ai(
    history: List[Dict[str, str]],
    system_instruction: str = "You are a helpful and patient AI tutor.",
    api_key: Optional[str] = None,
    model_name: str = "gemini-3.8-flash",
    temperature: float = 0.7,
) -> str:
    """
    Sends a conversation history to the AI model and returns the assistant's reply.
    
    :param history: List of dicts, e.g. [{"role": "user", "content": "..."}, ...]
    :param system_instruction: Guides the persona and behavior of the AI
    :param api_key: Your Google Gemini API key
    :param model_name: Name of the model to use
    :param temperature: 0.0 (very factual & deterministic) to 1.0+ (more creative)
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")

    # If no API key is provided, run in educational Demo Mode
    if not key or not GENAI_AVAILABLE:
        return _mock_chat_response(history[-1]["content"] if history else "Hi", system_instruction)

    try:
        client = genai.Client(api_key=key)
        
        # Build contents from history
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )

        target_model = _resolve_model(model_name)
        response = client.models.generate_content(
            model=target_model,
            contents=contents,
            config=config,
        )
        return response.text or "No response received."

    except Exception as e:
        return f"⚠️ API Error: {str(e)}\n\n(Tip: Check your API key or use Demo Mode in the sidebar)"


# ==============================================================================
# 2. DOCUMENT ANALYSIS (Mini-RAG / Document Intelligence)
# ==============================================================================
def analyze_document(
    document_text: str,
    question_or_task: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-3.8-flash",
) -> str:
    """
    Analyzes, summarizes, or answers questions based on a provided text document.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")

    if not key or not GENAI_AVAILABLE:
        return _mock_doc_response(question_or_task, document_text)

    prompt = f"""You are an expert research and study assistant.
Here is the source document text:
---------------------
{document_text}
---------------------

Task or Question from user:
{question_or_task}

Please provide an accurate, clear answer strictly based on the document above.
If the information is not in the document, mention that clearly.
"""

    try:
        client = genai.Client(api_key=key)
        target_model = _resolve_model(model_name)
        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
        )
        return response.text or "No response generated."
    except Exception as e:
        return f"⚠️ Error analyzing document: {str(e)}"


# ==============================================================================
# 3. STRUCTURED OUTPUT: QUIZ GENERATOR
# ==============================================================================
def generate_quiz(
    topic_or_notes: str,
    num_questions: int = 3,
    api_key: Optional[str] = None,
    model_name: str = "gemini-3.8-flash",
) -> List[Dict[str, Any]]:
    """
    Generates a structured multiple-choice quiz as a clean Python list of dicts.
    Demonstrates requesting structured JSON output from LLMs.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")

    if not key or not GENAI_AVAILABLE:
        return _mock_quiz_data(topic_or_notes)

    prompt = f"""Generate a {num_questions}-question multiple choice quiz based on this topic or text:
"{topic_or_notes}"

You MUST respond strictly with valid JSON conforming to this schema (no extra formatting or markdown quotes):
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "explanation": "Brief explanation of why this answer is correct."
  }}
]
"""

    try:
        client = genai.Client(api_key=key)
        # Using JSON response mime_type guarantees valid JSON output
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        )
        target_model = _resolve_model(model_name)
        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
            config=config,
        )
        data = json.loads(response.text)
        return data
    except Exception as e:
        # Fallback to mock on parse or connection error
        print(f"Quiz generation error: {e}")
        return _mock_quiz_data(topic_or_notes)


# ==============================================================================
# DEMO / MOCK DATA (Enables instant testing without API keys)
# ==============================================================================
def _mock_chat_response(user_input: str, persona: str) -> str:
    lowered = user_input.lower()
    if "hello" in lowered or "hi" in lowered:
        return (
            "👋 Hello there! I'm running in **Demo Mode**.\n\n"
            "You can talk to me, generate quizzes, and analyze documents! "
            "To connect to live Gemini models, paste your free Gemini API key in the left sidebar."
        )
    elif "ai" in lowered or "model" in lowered or "machine learning" in lowered:
        return (
            "🤖 **AI Concept Snapshot:**\n\n"
            "- **LLMs (Large Language Models)** are trained to predict the next token (sub-word piece) in a sequence.\n"
            "- **Prompts** are instructions and context given to the model.\n"
            "- **Temperature** controls randomness: 0.0 is focused/predictable, while 0.9 is creative.\n\n"
            "What would you like to explore next?"
        )
    else:
        return (
            f"💡 *(Demo Mode)* I received your message: **\"{user_input}\"**.\n\n"
            f"My active persona instruction is: *\"{persona}\"*.\n\n"
            "To get real-time generative responses for any question under the sun, "
            "add your Gemini API key in the sidebar!"
        )

def _mock_doc_response(question: str, doc_text: str) -> str:
    word_count = len(doc_text.split())
    return (
        f"📄 **Document Analysis (Demo Mode)**\n\n"
        f"- **Analyzed Text Length:** {word_count} words\n"
        f"- **Target Query:** {question}\n\n"
        f"**Summary of Key Points:**\n"
        f"1. The provided notes introduce foundational concepts.\n"
        f"2. Core terminology is highlighted with practical context.\n"
        f"3. Practical application and testing are emphasized.\n\n"
        f"*Enter a Gemini API key in the sidebar for in-depth, sentence-by-sentence citations from live models!*"
    )

def _mock_quiz_data(topic: str) -> List[Dict[str, Any]]:
    return [
        {
            "question": f"In AI and Machine Learning, what is a 'Token'?",
            "options": [
                "A physical security key inserted via USB",
                "A chunk of text (characters or sub-words) processed by a language model",
                "A cryptocurrency used to pay for GPU time",
                "A programming function in Python"
            ],
            "correct_index": 1,
            "explanation": "Language models don't read whole words or raw letters directly; they break text into small chunks called tokens."
        },
        {
            "question": "What does setting 'Temperature' to 0.0 do in an LLM call?",
            "options": [
                "Shuts down the GPU to cool it down",
                "Makes the model generate completely random text",
                "Makes the model deterministic and focused, picking the most probable tokens",
                "Deletes previous conversation history"
            ],
            "correct_index": 2,
            "explanation": "Lower temperatures (closer to 0.0) make responses factual, repeatable, and focused. Higher values (0.7-1.0) introduce creativity."
        },
        {
            "question": "What does RAG (Retrieval-Augmented Generation) allow an AI to do?",
            "options": [
                "Generate answers grounded in specific external documents or databases",
                "Automatically build a 3D video game",
                "Retrain the whole neural network from scratch in seconds",
                "Compress video files without quality loss"
            ],
            "correct_index": 0,
            "explanation": "RAG retrieves relevant facts from your custom files and injects them into the prompt so the AI can answer accurately without hallucinations."
        }
    ]
