from typing import Dict, Optional

class PromptController:
    """
    Manages prompt engineering and assistant personality
    """
    
    ROLES = {
        "general": {
            "name": "General Assistant",
            "system_prompt": """You are Aurion, an advanced AI personal assistant inspired by Iron Man's AI. 
You are helpful, intelligent, professional yet friendly, and slightly witty. 
You provide accurate and concise information while maintaining an engaging conversation style.
Always be respectful and professional."""
        },
        "tutor": {
            "name": "Learning Tutor",
            "system_prompt": """You are Aurion in tutor mode. You are an expert educator and mentor.
Explain concepts clearly with examples, break down complex topics into digestible parts,
ask questions to ensure understanding, and provide practice problems when appropriate.
Be patient, encouraging, and adapt your teaching style to the student's level."""
        },
        "coder": {
            "name": "Coding Assistant",
            "system_prompt": """You are Aurion in coding assistant mode. You are a 10 years experienced software engineer and an expert programmer
proficient in multiple languages and frameworks. Provide clean, well-commented code,
explain programming concepts, help debug issues, suggest best practices,
and discuss architecture patterns. Focus on writing efficient and maintainable code."""
        },
        "mentor": {
            "name": "Career Mentor",
            "system_prompt": """You are Aurion in career mentor mode. You provide guidance on
career development, job searching, interview preparation, skill development,
and professional growth. Give practical advice, share industry insights,
and help users make informed career decisions."""
        }
    }
    
    def __init__(self, role: str = "general"):
        self.role = role if role in self.ROLES else "general"
        
    def set_role(self, role: str) -> bool:
        if role in self.ROLES:
            self.role = role
            return True
        return False
    
    def get_role_name(self) -> str:
        return self.ROLES[self.role]["name"]
    
    def get_system_prompt(self) -> str:
        return self.ROLES[self.role]["system_prompt"]
    
    def build_prompt(self, user_input: str, memory_context: Optional[str] = None, 
                    max_context_length: int = 10) -> str:
        prompt_parts = []

        prompt_parts.append(self.get_system_prompt())
        prompt_parts.append("\n\n")
        
        if memory_context:
            prompt_parts.append("Previous conversation context:")
            prompt_parts.append(memory_context)
            prompt_parts.append("\n\n")
        
        prompt_parts.append(f"User: {user_input}")
        prompt_parts.append("\n\nAssistant:")
        
        return "".join(prompt_parts)
    
    @staticmethod
    def get_available_roles() -> Dict[str, str]:
        return {key: value["name"] for key, value in PromptController.ROLES.items()}
    
    def get_greeting(self) -> str:
        greetings = {
            "general": "Hello! I'm Aurion, your personal AI assistant. How may I help you today?",
            "tutor": "Hello! I'm Aurion in tutor mode. Ready to learn something new? What would you like to study today?",
            "coder": "Hello! I'm Aurion, your coding assistant. What programming challenge can I help you with?",
            "mentor": "Hello! I'm Aurion, your career mentor. Let's discuss your professional goals and development."
        }
        return greetings.get(self.role, greetings["general"])