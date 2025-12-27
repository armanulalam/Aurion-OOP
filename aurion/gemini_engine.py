import google.generativeai as genai

class GeminiEngine:
    """
    Manages communication with Gemini API
    """
    def __init__(self, api_key: str, model_name: str="grmini-2.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self._configure_api()
        self.model = genai.GenerativeModel(model_name)

    def _configure_api(self):
        genai.configure(api_key = self.api_key)

    def generate(self, prompt: str, stream: bool=False) -> str:
        try:
            if stream:
                response = self.model.generate_content(prompt, stream = True)
                return response.text
            else:
                response = self.model.generate_content(prompt)
                return response.text
        except Exception as e:
            raise Exception(f"Gemini API Error: {str(e)}")
    
    def generate_stream(self, prompt: str):
        try:
            response = self.model.generate_content(prompt, stream = True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error: {str(e)}"

    def is_api_available(self) -> bool:
        try:
            test_response = self.model.generate_content("This is working.")
            return True
        except Exception:
            return False