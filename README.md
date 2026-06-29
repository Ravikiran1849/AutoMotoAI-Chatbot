# 🏎️ AutoMotoAI — AI-Powered Automotive & Motorsport Chatbot

An intelligent customer and fan engagement chatbot for the automotive and motorsport industries, built with Flask and powered by Groq's Llama 3.3 70B model. Features real-time sentiment analysis, user personalization, and explainable AI responses.

## Features

- **Sentiment-Aware Responses** — Detects user mood using TextBlob and adapts tone accordingly (empathetic for frustration, enthusiastic for excitement)
- **User Personalization** — Automatically detects favourite car brands, racing teams, and interests from conversation to tailor future responses
- **Explainable AI (XAI)** — Every response comes with a transparent breakdown of why the chatbot responded the way it did
- **Domain Expertise** — Covers car buying advice, F1/MotoGP/NASCAR/WRC coverage, EV technology, maintenance tips, and fan engagement
- **Modern Web UI** — Dark-themed interface with live sentiment meter, explainability panel, and user profile sidebar

## Tech Stack

- **Backend:** Python, Flask
- **LLM:** Groq API (Llama 3.3 70B Versatile)
- **Sentiment Analysis:** TextBlob
- **Frontend:** HTML, CSS, JavaScript
- **Data Storage:** JSON-based user profiles

## Project Structure

```
AI_Chatbot_Project/
├── app.py                      # Flask application and routes
├── config.py                   # Configuration and environment variables
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── chatbot/
│   ├── __init__.py
│   ├── groq_client.py          # Groq API integration
│   ├── prompts.py              # System prompt engineering
│   ├── sentiment.py            # Sentiment analysis engine
│   ├── personalization.py      # User profiling and preference detection
│   └── explainability.py       # XAI explanation generator
├── templates/
│   └── index.html              # Chat interface
├── static/
│   ├── css/style.css           # UI styling
│   └── js/chat.js              # Frontend chat logic
└── data/                       # Runtime user profile storage
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ravikiran1849/AutoMotoAI-Chatbot.git
   cd AutoMotoAI-Chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open in browser:**
   ```
   http://localhost:5000
   ```

## How It Works

1. User sends a message through the web interface
2. **Sentiment Analysis** — TextBlob evaluates the emotional tone (polarity and subjectivity)
3. **Personalization** — The engine scans for brand names, team references, and topic interests to build a user profile
4. **Prompt Engineering** — A dynamic system prompt is constructed using the user's profile and detected sentiment
5. **LLM Response** — Groq's Llama 3.3 generates a context-aware, personalized response
6. **Explainability** — The XAI engine produces a human-readable explanation of the factors that shaped the response

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/`      | GET    | Serves the chat interface |
| `/chat`  | POST   | Processes user message and returns AI response with sentiment and explanation |
| `/reset` | POST   | Resets conversation history and user profile |

## License

This project is for academic and educational purposes.
