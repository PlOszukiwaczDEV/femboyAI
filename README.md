# FemboyAI Chatbot

FemboyAI is a friendly and professional AI assistant that speaks in UwU style while maintaining helpfulness. This chatbot uses the Groq API for generating responses and supports exporting and importing chat history.

## Features

- Speaks in UwU style with cute expressions
- Helpful and supportive personality
- Export and import chat history
- Handles `Ctrl+C` to gracefully exit the program
- Web-based UI with dark and light modes

## Requirements

- Python 3.6+
- `groq` library
- `python-dotenv` library
- `colorama` library
- `flask` library (Required for the API)
- `flask-cors` library (Required for CORS handling)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/PlOszukiwaczDEV/femboyAI.git
    cd femboyAI
    ```

2. Install the required libraries:
    ```sh
    pip install groq python-dotenv colorama flask flask-cors
    ```

3. Create a `.env` file in the project directory and add your Groq API key:
    ```env
    GROQ_API_KEY=your_groq_api_key
    ```

## Usage

### Chatbot

1. Run the chatbot:
    ```sh
    python main.py
    ```

2. Interact with the chatbot by typing your messages. Use the following commands for additional functionality:
    - `/export <filename>`: Export chat history to a file
    - `/import <filename>`: Import chat history from a file
    - `/stop`: Stop the chat session

### Flask API

1. Run the Flask API:
    ```sh
    python api.py
    ```

2. Interact with the API using the following endpoints:

#### Endpoints

##### GET /

Returns the HTML UI for the chatbot.

**Request:**
```sh
GET /
```

**Response:**
Returns the HTML page for the chatbot UI.

##### POST /chat

Send a message to the AI and receive a response.

**Request:**
```sh
POST /chat
Content-Type: application/json

{
    "message": "Hello!"
}
```

**Response:**
```json
{
    "response": "Hewwo! How can I hewp you today, uwu?"
}
```

## License

This project is licensed under the AGPL License. See the [LICENSE](LICENSE) file for details.