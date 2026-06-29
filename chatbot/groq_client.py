from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS, TEMPERATURE
from chatbot.prompts import build_system_prompt

client = Groq(api_key=GROQ_API_KEY)


def get_chat_response(user_message, chat_history, sentiment, user_profile):
    system_prompt = build_system_prompt(user_profile, sentiment)

    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=0.9,
            stream=False
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq API error: {e}")
        return (
            "I'm having trouble connecting right now. "
            "Please try again in a moment — I'm here to help with anything "
            "automotive or motorsport related!"
        )