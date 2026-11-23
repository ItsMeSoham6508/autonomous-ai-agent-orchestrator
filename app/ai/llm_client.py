from abc import ABC, abstractmethod


class LLMClient(ABC):
    def __init__(self, role: str, instructions: str, history: str, base_url: str, model: str):
        super().__init__()
        self.role = role
        self.instructions = instructions
        self.history = history
        self.base_url = base_url
        self.model = model

    @abstractmethod
    async def generate_response(self, inputs):
        pass