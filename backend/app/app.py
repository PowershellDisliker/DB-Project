from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .dto import LoginRequest

def run() -> FastAPI: 
    app = FastAPI()

    origins = [
        "http://localhost:5173"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Login route, used by Login page
    @app.post("/login")
    async def login(request: LoginRequest):
        if request.user_attempt == "test" and request.pass_attempt == "test":
            return {"success": True}
        return {"success": False}

    return app