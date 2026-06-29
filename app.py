from flask import Flask, render_template, request, jsonify, session
import uuid
from config import SECRET_KEY
from chatbot.groq_client import get_chat_response
from chatbot.sentiment import analyze_sentiment
from chatbot.personalization import PersonalizationEngine
from chatbot.explainability import ExplainabilityEngine

app = Flask(__name__)
app.secret_key = SECRET_KEY

personalization = PersonalizationEngine()
explainability = ExplainabilityEngine()


@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
        session["chat_history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    user_id = session.get("user_id", "anonymous")
    chat_history = session.get("chat_history", [])

    # Step 1: Sentiment Analysis
    sentiment_result = analyze_sentiment(user_message)

    # Step 2: Get/Update User Profile
    user_profile = personalization.get_profile(user_id)
    personalization.update_profile(user_id, user_message, sentiment_result)

    # Step 3: Get Chatbot Response from Groq
    bot_response = get_chat_response(
        user_message=user_message,
        chat_history=chat_history,
        sentiment=sentiment_result,
        user_profile=user_profile
    )

    # Step 4: Generate Explanation
    explanation = explainability.generate_explanation(
        user_message=user_message,
        sentiment=sentiment_result,
        user_profile=user_profile
    )

    # Step 5: Update Chat History in Session
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": bot_response})
    session["chat_history"] = chat_history[-20:]  # keep last 10 exchanges

    return jsonify({
        "response": bot_response,
        "sentiment": sentiment_result,
        "explanation": explanation
    })


@app.route("/reset", methods=["POST"])
def reset():
    user_id = session.get("user_id")
    session["chat_history"] = []
    if user_id:
        personalization.reset_profile(user_id)
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)