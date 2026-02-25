# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agent import route_user_message

app = FastAPI()

class Query(BaseModel):
    message: str
    user_id: str = "default_user"  # optional, defaults to single user for testing


@app.post("/ask")
async def ask(query: Query):
    try:
        response_text, tool_called = route_user_message(query.user_id, query.message)
        return {
            "response": response_text,
            "tool_called": tool_called
        }
    except Exception as e:
        # Catch any error to prevent frontend crash
        return {
            "response": "Oops! Something went wrong. Please try again.",
            "tool_called": "Error"
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )