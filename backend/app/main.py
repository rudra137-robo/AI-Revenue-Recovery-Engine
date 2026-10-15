import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from recovery import RecoveryEngine
from agents import RecoveryAgent

app = FastAPI(
    title="Razorpay AI Revenue Recovery Engine",
    description="Agentic engine for payment failure diagnosis and dynamic AI-driven interventions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RecoveryEngine()
agent = RecoveryAgent()

class TransactionRequest(BaseModel):
    payment_id: str
    merchant_id: str
    customer_id: str
    amount: float
    currency: str = "INR"
    payment_method: str
    payment_status: str
    failure_reason: Optional[str] = ""
    retry_count: int = 0
    checkout_attempted: bool = True

@app.get("/")
def root():
    return {
        "status": "online",
        "engine": "Razorpay AI Revenue Recovery Engine",
        "track": "Track 3: AI Revenue Recovery"
    }

@app.get("/api/recovery/summary")
def get_recovery_summary():
    try:
        summary = engine.process_batch_recovery()
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recovery/diagnose")
def diagnose_single_transaction(tx: TransactionRequest):
    try:
        record = tx.dict()
        recommendation = engine.diagnose_and_recommend(record)
        
        # Generate LLM-powered agentic recovery nudge message
        ai_nudge_message = agent.generate_agentic_nudge(record, recommendation)

        return {
            "status": "success",
            "payment_id": tx.payment_id,
            "intervention": recommendation,
            "ai_agent_nudge": ai_nudge_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))