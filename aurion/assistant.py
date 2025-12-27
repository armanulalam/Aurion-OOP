from typing import Optional, Generator
from .gemini_engine import GeminiEngine
from .prompt_controller import PromptController
from .memory import Memory

class Assistant:
    def __init__(self, engine: GeminiEngine, prompt_controller: PromptController, 
                 memory: Memory):
        """
        Initialize Assistant
        
        Args:
            engine: GeminiEngine instance for AI generation
            prompt_controller: PromptController for managing prompts
            memory: Memory instance for conversation history
        """
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory
        self._context_window = 10  # Number of previous messages to include
        
    def respond(self, user_input: str, conversation_id: Optional[str] = None) -> str:
        try:
            self.memory.add("user", user_input, conversation_id)
            
            context = self.memory.get_formatted_history(
                conversation_id=conversation_id, 
                limit=self._context_window
            )
            
            prompt = self.prompt_controller.build_prompt(user_input, context)

            response = self.engine.generate(prompt)

            self.memory.add("assistant", response, conversation_id)
            
            return response
            
        except Exception as e:
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            self.memory.add("assistant", error_message, conversation_id)
            return error_message
    
    def respond_stream(self, user_input: str, conversation_id: Optional[str] = None) -> Generator[str, None, None]:
        try:
            self.memory.add("user", user_input, conversation_id)

            context = self.memory.get_formatted_history(
                conversation_id=conversation_id,
                limit=self._context_window
            )
            
            prompt = self.prompt_controller.build_prompt(user_input, context)
            
            full_response = []
            for chunk in self.engine.generate_stream(prompt):
                full_response.append(chunk)
                yield chunk
            
            complete_response = "".join(full_response)
            self.memory.add("assistant", complete_response, conversation_id)
            
        except Exception as e:
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            self.memory.add("assistant", error_message, conversation_id)
            yield error_message
    
    def set_role(self, role: str) -> bool:
        return self.prompt_controller.set_role(role)
    
    def get_current_role(self) -> str:
        return self.prompt_controller.get_role_name()
    
    def get_greeting(self) -> str:
        return self.prompt_controller.get_greeting()
    
    def clear_memory(self, conversation_id: Optional[str] = None) -> None:
        self.memory.clear(conversation_id)
    
    def get_conversation_count(self, conversation_id: Optional[str] = None) -> int:
        return self.memory.get_message_count(conversation_id)
    
    def set_context_window(self, size: int) -> None:
        self._context_window = max(1, min(size, 50))  # Limit between 1 and 50