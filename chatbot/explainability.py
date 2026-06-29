class ExplainabilityEngine:

    def generate_explanation(self, user_message, sentiment, user_profile):
        factors = []

        # Sentiment factor
        label = sentiment["label"]
        polarity = sentiment["polarity"]
        if label in ("Very Negative", "Negative"):
            factors.append(
                f"Your message tone was detected as {label.lower()} "
                f"(polarity: {polarity}), so the response was adjusted "
                f"to be more empathetic and solution-oriented."
            )
        elif label in ("Positive", "Very Positive"):
            factors.append(
                f"Your message tone was detected as {label.lower()} "
                f"(polarity: {polarity}), so the response matches "
                f"your enthusiasm."
            )
        else:
            factors.append(
                f"Your message had a neutral tone (polarity: {polarity}), "
                f"so a balanced, informative response was provided."
            )

        # Personalization factors
        if user_profile.get("interests"):
            factors.append(
                f"Response was tailored to your known interests: "
                f"{', '.join(user_profile['interests'][:3])}."
            )
        if user_profile.get("favourite_brands"):
            factors.append(
                f"Your preferred brands ({', '.join(user_profile['favourite_brands'][:3])}) "
                f"were considered in the response."
            )
        if user_profile.get("favourite_teams"):
            factors.append(
                f"Your favourite teams ({', '.join(user_profile['favourite_teams'][:3])}) "
                f"were factored in."
            )

        # Interaction history
        count = user_profile.get("interaction_count", 0)
        if count > 5:
            factors.append(
                f"As a returning user ({count} interactions), the response "
                f"builds on your conversation history."
            )
        elif count == 0:
            factors.append(
                "As a new user, the response provides broad introductory "
                "information to learn your preferences."
            )

        return {
            "factors": factors,
            "summary": " | ".join(factors),
        }