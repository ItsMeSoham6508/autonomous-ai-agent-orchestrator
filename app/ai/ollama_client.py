import os
from typing import List, override
import httpx
from ollama import ChatResponse, chat
from pydantic import BaseModel
from app.ai.config_parser import config_save
from app.ai.llm_client import LLMClient
from app.enums.tool import Tool

class ToolResponse(BaseModel):
    tools_needed: List[Tool]

class OllamaClient(LLMClient):
    def __init__(
        self,
        role: str,
        instructions: str,
        history: list[dict[str, str]],
        model: str,
    ):
        super().__init__(role, instructions, history, os.getenv("OLLAMA_URL"), model)

    @override
    async def generate_response(self, inputs):
        self.history.append({"role": "user", "content": inputs["prompt"]})
        tools_needed = await self.desire_run_tool(inputs['prompt'], self.history)

        response: ChatResponse = chat(
            model=self.model,
            messages=self.history,
            options={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 20,
                "repeat_penalty": 1.05,
                "num_ctx": 16384
            }
        )
        if not response:
            raise RuntimeError("Ollama returned an empty response")
        return response.message.content

    @override
    async def run_tool(self, tool_type: Tool, inputs):
        if (tool_type == Tool.WEB_SEARCH):
            formatted_inputs = {
                "query": inputs
            }

        return await super().run_tool(tool_type, formatted_inputs)

    @override
    async def desire_run_tool(self, prompt: str, messages):
        tool_list = [Tool.WEB_SEARCH]
        prmpt = f"""
        You are given the following tools: {str(tool_list)}
        You may choose which ones you want to fulfill this users request: {str(messages)}
        """
        print(prmpt)
        tool_response: ChatResponse = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prmpt
                }
            ],
            format=ToolResponse.model_json_schema()
        )
        return tool_response.message.content

        

    