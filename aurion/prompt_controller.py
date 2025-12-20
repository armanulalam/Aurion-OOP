class PromptController:
    """
    Controls assistant behavior, role, and prompt formatting
    """

    def __init__(self, role: str = "assistant"):
        self.role =  role.lower()

    def build_prompt(self, user_input : str, memory : list) -> str:
        """
        Builds a structured prompt including:
        - System instruction
        - Assistant role
        - Conversation memory
        - User's current question
        """
        system_instruction = self._get_system_instruction()
        conversation = self._format_memory
        prompt = f""" 
        {system_instruction}

        Conversation History:
        {conversation}

        User Question:
        {user_input}
        """
    def _get_system_instruction(self) -> str:
        if self.role == "tutor":
            return (
                """You are Aurion, a friendly and patient tutor.
                Explain concepts step-by-step with simple examples."""
            )
        elif self.role == "coder":
            return (
                """You are Aurion, an expert software developer.
                Provide clean, effiecient, and well-commented code."""
            )
        elif self.role == "mentor":
            return(
                """"You are Aurion, a professional career mentor.
                Give practical advice, roadmaps, and motivation."""
            )
        else:
            return (
            """You are Aurion, a helpful and intelligent AI assistant.
            Answer questions clearly and concisely."""
        )

    def _format_memory(self, memory : list) -> str:
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