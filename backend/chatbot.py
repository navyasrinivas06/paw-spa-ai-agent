from pathlib import Path
from google import genai
from dotenv import load_dotenv
import os

# Store conversation history
conversation_memory = {}
booking_state = {}

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")
print("API Key loaded:", api_key[:10] + "..." if api_key else "None")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Load business information
data_folder = Path(__file__).parent / "business_data"

business_info = ""

for file in sorted(data_folder.glob("*.txt")):
    business_info += f"\n\n===== {file.stem.upper()} =====\n"
    business_info += file.read_text(encoding="utf-8")

def get_booking(session_id: str):
    if session_id not in booking_state:
        booking_state[session_id] = {
            "name": None,
            "phone": None,
            "pet_name": None,
            "pet_type": None,
            "breed": None,
            "service": None,
            "date": None,
            "time": None
        }

    return booking_state[session_id]

def ask_ai(session_id: str, message: str):

    # Get previous conversation
    history = conversation_memory.get(session_id, [])

    history_text = "\n".join(history)

    prompt = f"""
You are the official AI Assistant for Paw Spa & Nest.

Your responsibilities are:

1. Answer customer questions about Paw Spa & Nest.
2. Help customers book grooming or boarding appointments.
3. If a customer wants to book an appointment, collect these details one by one:

- Customer Name
- Phone Number
- Pet Name
- Pet Type (Dog/Cat)
- Breed
- Required Service
- Preferred Date
- Preferred Time

Never ask all questions at once.

Ask only for the next missing detail.

Once all information has been collected, tell the customer:

Once all information has been collected, say:

"Thank you! I have collected all the required booking details. Our team will contact you shortly to confirm your appointment."

Do not say that the booking has been saved unless it has actually been saved.
Do not invent business information. Only use the provided Business Information.

Business Information:
{business_info}

Previous Conversation:
{history_text}

Customer:
{message}

Reply professionally.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    reply = response.text

    # Save conversation
    history.append(f"Customer: {message}")
    history.append(f"Assistant: {reply}")

    # Keep only the last 20 messages
    conversation_memory[session_id] = history[-20:]

    return reply