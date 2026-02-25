# tools.py
import ollama
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT


def query_medgemma(prompt: str) -> str:
    """
    Calls MedGemma model (Ollama). Returns an empathic mental health response.
    Falls back to a simple response if model not available.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist.
Respond empathetically, normalize emotions, and give practical guidance.
Always ask open-ended questions to explore the user's feelings."""
    try:
        response = ollama.chat(
            model='MedAIBase/MedGemma1.0:4b',  # change if not available
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={'num_predict': 350, 'temperature': 0.7, 'top_p': 0.9}
        )
        return response['message']['content'].strip()
    except Exception:
        # Fallback free response
        return "I hear you. Can you tell me more about how that makes you feel?"


def call_emergency() -> str:
    """
    Place an emergency call via Twilio if credentials exist.
    Otherwise, print a mock message for safe development.
    """
    try:
        # Check if all credentials are present
        if all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT]):
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.calls.create(
                to=EMERGENCY_CONTACT,
                from_=TWILIO_FROM_NUMBER,
                url="http://demo.twilio.com/docs/voice.xml"  # You can customize this XML
            )
            return "✅ Emergency call placed successfully."
        else:
            # Mock for missing credentials
            print("[MOCK] Emergency call would be placed here.")
            return "[MOCK] Emergency call would be placed here. (Set Twilio credentials in config.py to make real calls)"
    except Exception as e:
        print(f"[ERROR] Twilio call failed: {e}")
        return "❌ Failed to place emergency call."


def find_nearby_therapists_by_location(location: str) -> str:
    """
    Returns a fixed list of therapists (mocked for free testing).
    """
    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )