import json
import os

class Memory:
    """
    Handles conversation memory using JSON file storage
    """
    def __init__(self, file_path : str = "data/memory.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok =True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding = 'utf-8') as f:
                json.dump([], f)

    def add(self, role: str, message: str):
        memory = self.get_history()
        memory.append({"role": role, "message": message})

        with open(self.file_path, 'w', encoding = 'utf-8') as f:
            json.dump(memory, f, indent = 2)

    def get_history(self) -> list:
        try:
            with open(self.file_path, 'r', encoding = 'utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def clear(self):
        with open(self.file_path, 'w', encoding = 'utf-8') as f:
            json.dump([], f)