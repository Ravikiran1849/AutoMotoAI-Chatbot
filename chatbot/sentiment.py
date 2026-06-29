from textblob import TextBlob

SENTIMENT_THRESHOLDS = {
    "very_negative": -0.6,
    "negative": -0.2,
    "neutral_low": 0.2,
    "positive": 0.6,
}

EMOJI_MAP = {
    "Very Negative": "😠",
    "Negative": "😟",
    "Neutral": "😐",
    "Positive": "🙂",
    "Very Positive": "😄",
}


def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity <= SENTIMENT_THRESHOLDS["very_negative"]:
        label = "Very Negative"
    elif polarity <= SENTIMENT_THRESHOLDS["negative"]:
        label = "Negative"
    elif polarity <= SENTIMENT_THRESHOLDS["neutral_low"]:
        label = "Neutral"
    elif polarity <= SENTIMENT_THRESHOLDS["positive"]:
        label = "Positive"
    else:
        label = "Very Positive"

    confidence = min(abs(polarity) * 1.5, 1.0) if label != "Neutral" else 0.5

    return {
        "label": label,
        "score": round(confidence, 3),
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "emoji": EMOJI_MAP[label],
    }