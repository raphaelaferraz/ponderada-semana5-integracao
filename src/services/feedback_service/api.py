from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from .tests.circuit_breaker import circuit_breaker_process_feedback
from .feedback_repository import get_feedbacks

app = FastAPI()

class FeedbackRequest(BaseModel):
    motoboy_id: int
    response: str

@app.post("/feedback/")
async def receive_feedback(feedback: FeedbackRequest):
    try:
        resultado = await circuit_breaker_process_feedback(feedback.motoboy_id, feedback.response)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/feedbacks/")
def list_feedbacks():
    return get_feedbacks()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
