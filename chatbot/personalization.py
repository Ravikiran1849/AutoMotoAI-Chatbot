import json
import os
import re
from config import USER_PROFILES_PATH

DEFAULT_PROFILE = {
    "name": None,
    "interests": [],
    "favourite_brands": [],
    "favourite_teams": [],
    "sentiment_history": [],
    "interaction_count": 0,
}

BRAND_KEYWORDS = [
    "toyota", "honda", "bmw", "mercedes", "audi", "ford", "tesla",
    "porsche", "ferrari", "lamborghini", "mclaren", "hyundai", "kia",
    "volkswagen", "nissan", "mazda", "subaru", "lexus", "volvo",
    "jaguar", "land rover", "bentley", "rolls royce", "bugatti",
    "aston martin", "alfa romeo", "maserati", "chevrolet", "dodge",
]

TEAM_KEYWORDS = [
    "red bull", "mercedes amg", "ferrari f1", "mclaren f1", "alpine",
    "aston martin f1", "williams", "haas", "alfa romeo racing",
    "alphatauri", "rb", "kick sauber", "nascar", "indycar",
]

INTEREST_KEYWORDS = {
    "f1": "Formula 1", "formula 1": "Formula 1", "formula one": "Formula 1",
    "motogp": "MotoGP", "wrc": "WRC Rally", "nascar": "NASCAR",
    "le mans": "Le Mans/Endurance", "wec": "Le Mans/Endurance",
    "indycar": "IndyCar", "formula e": "Formula E",
    "ev": "Electric Vehicles", "electric car": "Electric Vehicles",
    "suv": "SUVs", "sedan": "Sedans", "sports car": "Sports Cars",
    "supercar": "Supercars", "hypercar": "Hypercars",
    "tuning": "Car Tuning/Mods", "modification": "Car Tuning/Mods",
    "drifting": "Drifting", "drag racing": "Drag Racing",
    "rally": "Rally", "karting": "Karting",
    "maintenance": "Car Maintenance", "restoration": "Classic Car Restoration",
}


class PersonalizationEngine:
    def __init__(self):
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        if os.path.exists(USER_PROFILES_PATH):
            with open(USER_PROFILES_PATH, "r") as f:
                return json.load(f)
        return {}

    def _save_profiles(self):
        os.makedirs(os.path.dirname(USER_PROFILES_PATH), exist_ok=True)
        with open(USER_PROFILES_PATH, "w") as f:
            json.dump(self.profiles, f, indent=2)

    def get_profile(self, user_id):
        return self.profiles.get(user_id, DEFAULT_PROFILE.copy())

    def update_profile(self, user_id, message, sentiment):
        profile = self.get_profile(user_id)
        msg_lower = message.lower()

        # Detect name from introduction
        if not profile["name"]:
            name_patterns = [
                r"(?:my name is|i'm|i am|call me)\s+([A-Z][a-z]+)",
            ]
            for pattern in name_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    profile["name"] = match.group(1).title()
                    break

        # Detect brands
        for brand in BRAND_KEYWORDS:
            if brand in msg_lower and brand.title() not in profile["favourite_brands"]:
                profile["favourite_brands"].append(brand.title())

        # Detect teams
        for team in TEAM_KEYWORDS:
            if team in msg_lower and team.title() not in profile["favourite_teams"]:
                profile["favourite_teams"].append(team.title())

        # Detect interests
        for keyword, interest in INTEREST_KEYWORDS.items():
            if keyword in msg_lower and interest not in profile["interests"]:
                profile["interests"].append(interest)

        # Track sentiment
        profile["sentiment_history"].append(sentiment["label"])
        profile["sentiment_history"] = profile["sentiment_history"][-20:]
        profile["interaction_count"] += 1

        self.profiles[user_id] = profile
        self._save_profiles()

    def reset_profile(self, user_id):
        if user_id in self.profiles:
            del self.profiles[user_id]
            self._save_profiles()