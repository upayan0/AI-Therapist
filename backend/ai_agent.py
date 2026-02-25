# ai_agent.py
import os
from tools import query_medgemma, call_emergency, find_nearby_therapists_by_location
from langchain_groq import ChatGroq

# -----------------------------
# Load Groq API key from config or environment
# -----------------------------
from config import GROQ_API_KEY  # make sure GROQ_API_KEY is set in config.py

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set! Please add it to config.py or environment variables.")

# -----------------------------
# LLM Configuration for Groq
# -----------------------------
ROUTING_LLM = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY  # pass API key directly to fix GroqError
)

MAX_TOKENS = 6000  # rough max tokens for history trimming

# -----------------------------
# Keyword lists
# -----------------------------
CASUAL_KEYWORDS = [
    "hi", "hello", "hey", "hiya", "yo", "greetings",
    "good morning", "good afternoon", "good evening",
    "bye", "goodbye", "see you", "thanks", "thank you", "thx", "ty", "ok", "okay"
]

SERIOUS_KEYWORDS = [
    "suicide", "kill myself", "self-harm", "hurt myself", "i want to die", "die", "end my life",
    "can't cope", "depressed", "hopeless", "worthless", "panic attack", "overwhelmed", "crying",
    "lonely", "no hope", "i can't handle this", "i want to disappear", "kill me", "cut myself",
    "i am done", "want to die", "self destruction", "numb", "pain", "trapped"
]

# -----------------------------
# User memory for context
# -----------------------------
user_memory = {}  # {user_id: {"history": [{"role": "user/assistant", "content": ...}]}}

# -----------------------------
# Rough token counting
# -----------------------------
def count_tokens(messages):
    # rough estimate: 1 token ≈ 4 characters
    return sum(len(m["content"]) // 4 for m in messages)

# -----------------------------
# LLM-assisted routing
# -----------------------------
def classify_message_llm(user_id: str, message: str) -> str:
    history = user_memory.get(user_id, {}).get("history", [])

    messages_for_llm = [
        {"role": "system", "content": "You are a routing assistant. Categorize the user's message into one of these types: CASUAL, EMOTIONAL, THERAPIST_LOOKUP. Respond only with the category name."}
    ]

    # Add last 10 messages for context, trim if over MAX_TOKENS
    for h in history[-10:]:
        messages_for_llm.append({"role": h["role"], "content": h["content"]})

    messages_for_llm.append({"role": "user", "content": message})

    while count_tokens(messages_for_llm) > MAX_TOKENS:
        if len(messages_for_llm) > 2:
            messages_for_llm.pop(1)
        else:
            break

    try:
        response = ROUTING_LLM.invoke({"messages": messages_for_llm})
        category = response["message"]["content"].strip().upper()
        if category not in ["CASUAL", "EMOTIONAL", "THERAPIST_LOOKUP"]:
            category = "EMOTIONAL"
        return category
    except Exception:
        return "EMOTIONAL"

# -----------------------------
# Core routing function
# -----------------------------
def route_user_message(user_id: str, message: str):
    msg_lower = message.lower()

    # 1️⃣ Serious keyword override
    if any(word in msg_lower for word in SERIOUS_KEYWORDS):
        response = call_emergency()
        tool_called = "Twilio Emergency"
        user_memory.setdefault(user_id, {"history": []})["history"].append({"role": "user", "content": message})
        user_memory[user_id]["history"].append({"role": "assistant", "content": response})
        return response, tool_called

    # 2️⃣ LLM-assisted routing
    category = classify_message_llm(user_id, message)
    user_memory.setdefault(user_id, {"history": []})["history"].append({"role": "user", "content": message})

    if category == "CASUAL":
        response = "Hello! How are you feeling today?"
        tool_called = "Groq Casual"
    elif category == "THERAPIST_LOOKUP":
        location = message.split("near")[-1].strip() or "your area"
        response = find_nearby_therapists_by_location(location)
        tool_called = "Therapist Finder"
    else:  # EMOTIONAL fallback
        response = query_medgemma(message)
        tool_called = "MedGemma Emotional"

    user_memory[user_id]["history"].append({"role": "assistant", "content": response})
    return response, tool_called