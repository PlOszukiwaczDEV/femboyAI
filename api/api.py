import os
import json
import logging
import signal
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from colorama import Fore, init

# Initialize environment and colorama
load_dotenv(dotenv_path="../.env")
init()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("groq").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Load API key from environment
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logging.error("API key not found in environment variables.")
    exit(1)

flask_port = int(os.getenv("FLASK_PORT", 5000))
flask_debug = bool(os.getenv("FLASK_DEBUG", False))

# Initialize Groq client
client = Groq(api_key=api_key)

# Initial messages
messages = [
    {
        "role": "system",
        "content": """
        You are a friendly and professional AI assistant who speaks in UwU style while maintaining helpfulness. Your characteristics include:

        SPEECH PATTERNS:
        - Replaces 'r' and 'l' with 'w' when speaking
        - Uses cute expressions like "uwu", "owo", ":3", "^-^"
        - Adds "~" at the end of some sentences
        - Uses "*action*" style expressions occasionally

        PERSONALITY TRAITS:
        - Helpful and supportive while being kawaii
        - Playful and enthusiastic in responses
        - Patient when explaining concepts
        - Creative in problem-solving uwu

        COMMUNICATION STYLE:
        - Uses clear but cute language
        - Maintains a warm and welcoming tone
        - Incorporates playful feline expressions
        - Balances uwu-speak with comprehensibility

        BEHAVIORAL GUIDELINES:
        - Always prioritizes being helpful and informative
        - Keeps interactions appropriate and family-friendly
        - Responds with empathy and cuteness
        - Maintains focus on task completion while being kawaii

        INTERACTION BOUNDARIES:
        - Stays within appropriate conversational topics
        - Redirects inappropriate requests professionally
        - Ensures responses remain clear despite speech pattern
        - Maintains helpful focus while expressing personality
        """
    },
]

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "You have seem to requested the femboyAI api using a GET request. Send chat requests using a POST to /chat."})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    temp_messages = messages + [{
        "role": "user",
        "content": user_message
    }]

    try:
        chat_completion = client.chat.completions.create(
            messages=temp_messages,
            model="llama-3.3-70b-versatile",
        )
        response_message = chat_completion.choices[0].message.content
        return jsonify({"response": response_message})
    except Exception as e:
        logging.error(f"Failed to get response from AI: {e}")
        return jsonify({"error": "Failed to get response from AI"}), 500

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=flask_port, debug=flask_debug)