from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from app.interfaces.regex_controller import RegexController


class Application:
    def __init__(self):
        self.app = FastAPI()
        self._configure_logging()
        self._configure_middleware()
        self._configure_routes()

    def _configure_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _configure_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _configure_routes(self):
        controller = RegexController()
        self.app.get("/", response_class=HTMLResponse)(controller.get_root)
        self.app.post("/generate")(controller.generate_regex)
        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    Application().run()
