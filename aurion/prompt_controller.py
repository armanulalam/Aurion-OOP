class BasePrompt:
    """
    Base class defining common prompt behavior
    """
    def system_instruction(self) -> str:
        return (
            """You are Aurion, a helpful and intelligent AI assistant.
            Answer questions clearly and concisely."""
        )
    def format_memory(self, memory : list) -> str:
        """
        Converts memory list into readable conversation format
        """
        if not memory:
            return "No previous conversation."

        formatted= []
        
        for i in memory:
            role = i.get("role", "user").capitalize()
            text = i.get("message", "")
            formatted.append(f"{role}: {message}")

        return "\n".join(formatted)

class TutorPrompt(BasePrompt):
    def get_system_instruction(self) -> str:
        return (
                """You are Aurion, a friendly and patient tutor.
                Explain concepts step-by-step with simple examples."""
            )

class CoderPrompt(BasePrompt):
    def get_system_instruction(self) -> str:
        return (
                """You are Aurion, an expert software developer.
                Provide clean, effiecient, and well-commented code."""
            )

class MentorPrompt(BasePrompt):
    def get_system_instruction(self) -> str:
        return(
                """"You are Aurion, a professional career mentor.
                Give practical advice, roadmaps, and motivation."""
            )

class PromptController:
    """
    Controls assistant behavior, role, and prompt formatting
    """

    def __init__(self, role: str = "assistant"):
        self.prompt_strategy = self._select_prompt(role)

    def _select_prompt(self, role: str):
        role = role.lower()

        if role == "tutor":
            return TutorPrompt()
        elif role == "coder":
            return CoderPrompt()
        elif role == "mentor":
            return MentorPrompt()
        else:
            return BasePrompt()

    def build_prompt(self, user_input : str, memory : list) -> str:
        """
        Builds a structured prompt including:
        - System instruction
        - Assistant role
        - Conversation memory
        - User's current question
        """
        system_instruction = self.prompt_strategy.get_system_instruction()
        conversation = self.prompt_strategy.format_memory(memory)
        prompt = f""" 
        {system_instruction}

        Conversation History:
        {conversation}

        User Question:
        {user_input}

        Assistant Response:
        """
        return prompt.strip() 