import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1024
TEMPERATURE = 0.7
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USER_PROFILES_PATH = os.path.join(DATA_DIR, "user_profiles.json")