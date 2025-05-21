from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.regex_service import RegexService
import logging

class RegexController:
    def __init__(self):
        self.regex_service = RegexService()
        self.logger = logging.getLogger(__name__)

    async def get_root(self):
        try:
            with open("static/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(f.read())
        except FileNotFoundError:
            return HTMLResponse("<h1>Index file not found</h1>", status_code=404)

    async def generate_regex(self, request: Request):
        data = await request.json()
        self.logger.info(f"Received request: {data}")

        problem = data.get("problem")
        if not problem:
            return JSONResponse(content={"error": "No input provided"}, status_code=400)

        try:
            regex = await self.regex_service.generate_regex(problem)
            return {"regex": regex}
        except Exception as e:
            self.logger.exception("Error generating regex")
            return JSONResponse(content={"error": str(e)}, status_code=500)
