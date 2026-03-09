import httpx


class ReportClient:

    BASE_URL = "http://localhost:8002"

    async def send(self, message: str, session_id: str | None):

        async with httpx.AsyncClient(timeout=180) as client:

            response = await client.post(
                f"{self.BASE_URL}/llm/chat",
                json={
                    "message": message,
                    "session_id": session_id
                }
            )

        return response.json()