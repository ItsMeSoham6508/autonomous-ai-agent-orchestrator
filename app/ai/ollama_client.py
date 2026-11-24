import os
from typing import override
import httpx
from app.ai.llm_client import LLMClient
from app.enums.tool import Tool

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
        messages = [{"role": "system", "content": f"{self.role}\n{self.instructions}"}]
        messages.extend(
            {
                "role": "assistant" if item["role"] == "ai" else item["role"],
                "content": item["message"],
            }
            for item in self.history
            if isinstance(item, dict)
            and item.get("role") in {"user", "ai", "assistant"}
            and isinstance(item.get("message"), str)
            and item["message"]
        )
        messages.append({"role": "user", "content": inputs["prompt"]})

        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                self.base_url + "/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0},
                },
            )
        response.raise_for_status()
        content = response.json()["message"]["content"]
        if not content:
            raise RuntimeError("Ollama returned an empty response")
        return content

    @override
    async def run_tool(self, tool_type: Tool, inputs):
        if (tool_type == Tool.WEB_SEARCH):
            formatted_inputs = {
                "query": inputs
            }

        return await super().run_tool(tool_type, formatted_inputs)

    