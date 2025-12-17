import google.generativeai as genai
from config.settings import Settings

class GeminiEngine():
    """
    Handles communication with Gemini API Key
    """
    def __init__(self):
        settings = Settings()

        genai.configure(api_key = settings.get_gemini_api_key())
        self.model = genai.GenerativeModel(settings.get_model_name())

    def generate(self,prompt:str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini API Error: {str(e)}"