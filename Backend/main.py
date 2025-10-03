from fastapi import FastAPI
from pydantic import BaseModel
from src.config.ConfigHelper import ConfigHelper
from src.handlers.AnswerGenerator import AnswerGenerator
from src.middleware.PrefixMiddleware import PrefixMiddleware
import uvicorn
import warnings
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware # 1. IMPORT THIS

warnings.filterwarnings("ignore")

__config = ConfigHelper().config
answer_gen = AnswerGenerator()

app = FastAPI()

# 2. ADD CORS MIDDLEWARE BLOCK
# This is essential for allowing your React frontend to communicate with this backend
origins = [
    "http://localhost",
    "http://localhost:3000",  # The default port for create-react-app
    # Add any other origins you might use for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)
# --- END OF CORS BLOCK ---


app.add_middleware(
    PrefixMiddleware, prefix="/" + __config["service_discovery"]["app"]["app_name"]
)

@app.get("/info")
def get_home() -> str:
    """Returns a welcome message for the chatbot."""
    return "Loan Assistance ChatBot"

@app.get("/health")
def health() -> dict:
    """Returns the health status of the application."""
    return {"status": "UP", "components": {"status": "UP"}}

class ChatRequest(BaseModel):
    query: str

@app.post("/response")
async def chatbot_answer(request: ChatRequest) -> dict:
    """Generates an answer for a given query."""
    response = answer_gen.generate_answer(
        request.query
    )
    return JSONResponse(content=response)

if __name__ == "__main__":
    # Ensure the host is set to "0.0.0.0" or "127.0.0.1" for local access
    host = "0.0.0.0" 
    port = __config["service_discovery"]["app"]["instance_port"]
    print("--- Loan Assistant Backend ---")
    print(
        f"Running on: http://{host}:{port}"
    )
    print(
        f"API Endpoint available at: http://{host}:{port}/{__config['service_discovery']['app']['app_name']}/response"
    )
    uvicorn.run("main:app", host=host, port=port, reload=True)
