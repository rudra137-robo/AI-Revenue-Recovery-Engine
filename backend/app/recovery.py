import os
import json
import pandas as pd
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_data.csv")

class RecoveryEngine:
    def __init__(self, data_path: str = DEFAULT_DATA_PATH):
        self.data_path = data_path

    def load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at path: {self.data_path}")

        df = pd.read_csv(self.data_path)
        
        # Replace NaN values (like empty failure_reason) with empty strings so JSON serialization doesn't crash
        df = df.fillna("")

        if 'faliure_reason' in df.columns and 'failure_reason' not in df.columns:
            df.rename(columns={'faliure_reason': 'failure_reason'}, inplace=True)
        if 'payment_methord' in df.columns and 'payment_method' not in df.columns:
            df.rename(columns={'payment_methord': 'payment_method'}, inplace=True)
        return df

    def diagnose_and_recommend(self, record: Dict[str, Any]) -> Dict[str, Any]:
        status = record.get("payment_status")
        reason = str(record.get("failure_reason", "")).upper()
        retries = int(record.get("retry_count", 0)) if record.get("retry_count") != "" else 0
        amount = float(record.get("amount", 0)) if record.get("amount") != "" else 0.0

        if status == "SUCCESS":
            return {
                "action": "NONE",
                "strategy": "Payment already successful",
                "recovery_probability": 0.0,
                "expected_recovery_amount": 0.0
            }

        if reason in ["NETWORK_ERROR", "BANK_TIMEOUT", "GATEWAY_TIMEOUT", "TEMPORARY_BANK_DECLINE"]:
            if retries < 3:
                return {
                    "action": "SMART_RETRY",
                    "strategy": "Schedule automatic API retry in 15 minutes via secondary gateway",
                    "recovery_probability": 0.85,
                    "expected_recovery_amount": amount * 0.85
                }
            else:
                return {
                    "action": "SEND_ALTERNATIVE_LINK",
                    "strategy": "Exceeded automatic retries. Send WhatsApp link to complete payment via UPI",
                    "recovery_probability": 0.50,
                    "expected_recovery_amount": amount * 0.50
                }

        elif reason == "INSUFFICIENT_FUNDS":
            return {
                "action": "OFFER_PAY_LATER",
                "strategy": "Trigger automated notification suggesting Pay Later / EMI or retry on salary date",
                "recovery_probability": 0.40,
                "expected_recovery_amount": amount * 0.40
            }

        elif status == "ABANDONED" or reason == "CHECKOUT_ABANDONED":
            discount = 10 if amount > 3000 else 5
            return {
                "action": "DYNAMIC_DISCOUNT_NUDGE",
                "strategy": f"Send personalized offer link with {discount}% instant discount valid for 2 hours",
                "recovery_probability": 0.60,
                "expected_recovery_amount": (amount * (1 - discount/100)) * 0.60
            }

        elif reason in ["CARD_EXPIRED", "AUTHENTICATION_REQUIRED", "INVALID_PAYMENT_DETAILS", "PAYMENT_DECLINED"]:
            return {
                "action": "PROMPT_NEW_PAYMENT_METHOD",
                "strategy": "Send instant push/SMS prompt to update card details or select UPI/NetBanking",
                "recovery_probability": 0.45,
                "expected_recovery_amount": amount * 0.45
            }

        elif reason == "FRAUD_DETECTED":
            return {
                "action": "HUMAN_AUDIT_REQUIRED",
                "strategy": "Flagged for manual compliance audit. Do not auto-retry.",
                "recovery_probability": 0.0,
                "expected_recovery_amount": 0.0
            }

        return {
            "action": "GENERIC_RECOVERY_LINK",
            "strategy": "Send standard payment recovery link",
            "recovery_probability": 0.30,
            "expected_recovery_amount": amount * 0.30
        }

    def process_batch_recovery(self) -> Dict[str, Any]:
        df = self.load_data()
        results = []
        total_failed_volume = 0.0
        total_projected_recovery = 0.0
        action_counts = {}

        for _, row in df.iterrows():
            record = row.to_dict()
            if record.get("payment_status") != "SUCCESS":
                total_failed_volume += float(record.get("amount", 0))
            
            recommendation = self.diagnose_and_recommend(record)
            action = recommendation["action"]
            action_counts[action] = action_counts.get(action, 0) + 1
            
            total_projected_recovery += recommendation["expected_recovery_amount"]
            results.append({**record, **recommendation})

        recovery_rate = (total_projected_recovery / total_failed_volume * 100) if total_failed_volume > 0 else 0

        return {
            "total_records_processed": len(df),
            "total_failed_amount_inr": round(total_failed_volume, 2),
            "total_projected_recovery_inr": round(total_projected_recovery, 2),
            "projected_recovery_rate_pct": round(recovery_rate, 2),
            "action_breakdown": action_counts,
            "sample_recoveries": results[:10]
        }

if __name__ == "__main__":
    engine = RecoveryEngine()
    summary = engine.process_batch_recovery()
    print(json.dumps(summary, indent=2))