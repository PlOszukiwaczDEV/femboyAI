import os
import json
import logging
import signal
from groq import Groq
from dotenv import load_dotenv
from colorama import Fore, init

# Initialize environment and colorama
load_dotenv()
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

def export_chat_history(filename):
    try:
        with open(filename, 'w') as file:
            json.dump(messages, file, indent=4)
        logging.info(f"Chat history exported to {filename}")
    except Exception as e:
        logging.error(f"Failed to export chat history: {e}")

def import_chat_history(filename):
    global messages
    try:
        with open(filename, 'r') as file:
            messages = json.load(file)
        logging.info(f"Chat history imported from {filename}")
    except Exception as e:
        logging.error(f"Failed to import chat history: {e}")

def clear_chat_history():
    global messages
    messages = [messages[0]]
    logging.info("Chat history cleared.")

def save_chat_on_exit():
    export_chat_history("chat_history.json")
    logging.info("Chat history saved on exit.")

def list_commands():
    commands = """
    Available commands:
    /export <filename> - Export chat history to a file
    /import <filename> - Import chat history from a file
    /clear - Clear the chat history
    /stop - Stop the chat session
    /help - List available commands
    """
    print(commands)

def handle_exit(signum, frame):
    save_chat_on_exit()
    logging.info("Exiting the chat session.")
    exit(0)

def main():
    signal.signal(signal.SIGINT, handle_exit)
    
    if os.path.exists("chat_history.json"):
        import_chat_history("chat_history.json")
        print(f"{Fore.YELLOW}Loaded chat history from chat_history.json, you can reset it using /clear{Fore.RESET}")

    while True:
        user_message = input(f"{Fore.GREEN}You: {Fore.RESET}")

        if user_message.startswith("/export"):
            try:
                _, filename = user_message.split(maxsplit=1)
                export_chat_history(filename)
            except ValueError:
                logging.warning("Please provide a filename to export chat history to")
            continue

        if user_message.startswith("/import"):
            try:
                _, filename = user_message.split(maxsplit=1)
                import_chat_history(filename)
            except ValueError:
                logging.warning("Please provide a filename to import chat history from")
            continue

        if user_message == "/clear":
            clear_chat_history()
            continue

        if user_message == "/stop":
            save_chat_on_exit()
            logging.info("Exiting the chat session.")
            break

        if user_message == "/help":
            list_commands()
            continue

        messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
            )
            response_message = chat_completion.choices[0].message.content
            print(f"{Fore.BLUE}AI: {response_message}{Fore.RESET}")

            messages.append({
                "role": "assistant",
                "content": response_message
            })
        except Exception as e:
            logging.error(f"Failed to get response from AI: {e}")

if __name__ == "__main__":
    main()