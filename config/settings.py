import os
from dotenv import load_dotenv

class Settings():
    """
    Central configuration handler for the application
    """
    def __init__(self):
        load_dotenv()

    def get_gemini_api_key(self) -> str:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")

        return api_key

    def get_model_name(self) -> str:
        return "gemini-2.5-flash"