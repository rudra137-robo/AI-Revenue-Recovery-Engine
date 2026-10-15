import os
from typing import Dict, Any
from litellm import completion

class RecoveryAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name

    def generate_agentic_nudge(self, record: Dict[str, Any], recommendation: Dict[str, Any]) -> str:
        """
        Uses an LLM to craft a hyper-personalized, context-aware recovery message
        tailored to the customer's failure reason and transaction amount.
        """
        customer_id = record.get("customer_id", "Customer")
        amount = record.get("amount", 0)
        failure_reason = record.get("failure_reason", "UNKNOWN")
        strategy = recommendation.get("strategy", "Retry payment")
        action = recommendation.get("action", "STANDARD_RETRY")

        # Fallback if API keys aren't set yet so the app never crashes during offline demo runs
        has_key = bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("LITELLM_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))
        
        if not has_key:
            return (
                f"[AI Fallback Nudge] Hi {customer_id}, we noticed your payment of ₹{amount} "
                f"did not go through due to {failure_reason}. Recommended fix: {strategy}. "
                f"Complete your checkout here: https://rzp.io/i/secure-recovery"
            )

        prompt = f"""
        You are an elite AI Revenue Recovery Agent for Razorpay. 
        Your goal is to recover failed merchant revenue by sending a polite, urgent, and highly persuasive WhatsApp/SMS nudge to a customer.

        Transaction Details:
        - Customer ID: {customer_id}
        - Amount: ₹{amount}
        - Failure Reason: {failure_reason}
        - Recommended Recovery Strategy: {strategy}
        - Action Type: {action}

        Instructions:
        1. Write a short, friendly, conversion-optimized recovery message (max 2-3 sentences).
        2. Acknowledge the specific friction point without sounding robotic.
        3. Include a placeholder secure payment link.
        """

        try:
            response = completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Hi {customer_id}, please retry your payment of ₹{amount}. Strategy: {strategy}"