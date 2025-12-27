import os
from dotenv import load_dotenv
from typing import Optional

class Settings:
    """
    Handles application configuration and environment variables
    """
    
    def __init__(self):
        load_dotenv()
        self._api_key: Optional[str] = None
        
    def load_api_key(self) -> str:
        if self._api_key is None:
            self._api_key = os.getenv("GEMINI_API_KEY")
            
        if not self._api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
            
        return self._api_key
    
    @staticmethod
    def get_data_dir() -> str:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        return data_dir