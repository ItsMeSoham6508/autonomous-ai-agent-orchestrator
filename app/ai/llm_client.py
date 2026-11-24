from abc import ABC, abstractmethod

from app.ai_tools.search_engine import Search
from app.enums.tool import Tool


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

    @abstractmethod
    async def run_tool(self, tool_type: Tool, inputs):
        if (tool_type == Tool.WEB_SEARCH):
            search = Search()
            results = search.search_json_format(inputs['query'])
            return results

    
    async def desire_run_tool(self, prompt: str):
        pass