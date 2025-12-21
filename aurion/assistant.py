from aurion.gemini_engine import GeminiEngine
from aurion.prompt_controller import PromptController
from aurion.memory import Memory

class Assistant:
    def __init__(self, role: str="assistant"):
        self.engine = GeminiEngine()
        self.memory = Memory()
        self.prompt_controller = PromptController(role)

    def respond(self, user_input:str) -> str:
        self.memory.add("user",user_input)
        prompt = self.prompt_controller.build_prompt(
            user_input=user_inpt,
            memory=self.memory.get_history()
        )

        response=self.engine.generate(prompt)
        self.memory.add("assistant",response)
        return response

    def clear_memory(self):
        self.memory.clear()