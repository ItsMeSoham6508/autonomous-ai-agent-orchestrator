import json
import os

from dotenv import load_dotenv
import httpx

class Search:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SEARXNG_CONTACT_URL")

    async def search_json_format(self, query: str):
        search_request = httpx.Request(
            "GET",
            self.url + "/search",
            params={
                "q": query,
                "format": "json"
            }
        )
        async with httpx.AsyncClient(timeout=120) as client:
            results = await client.send(search_request)

        return results.json()

    async def search_any_format(self, query: str, format: str):
        search_request = httpx.Request(
                    "GET",
                    self.url + "/search",
                    params={
                        "q": query,
                        "format": format
                    }
                )
        async with httpx.AsyncClient(timeout=120) as client:
            results = await client.send(search_request)

        return results
            