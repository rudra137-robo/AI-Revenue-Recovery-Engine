import os
import csv
import random 
from datetime import datetime, timedelta

random.seed(42)  

# Dynamic path resolution to project root 'data' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(DATA_DIR, "synthetic_data.csv")

headers = [
    "payment_id",
    "merchant_id",
    "customer_id",
    "amount",
    "currency",
    "payment_method",
    "payment_status",
    "failure_reason",
    "created_at",
    "retry_count",
    "checkout_attempted",
]

payment_methods = ["credit_card", "debit_card", "paypal", "bank_transfer"]

rows = []
start_date = datetime(2026, 8, 1)

for i in range(1, 101):
    amount = random.choice([499, 999, 1499, 2499, 3999, 4999, 7499, 9999, 14999, 24999])
    created_at = start_date + timedelta(minutes=random.randint(0, 30 * 24 * 60))
    
    scenario = random.choices(
        ["SUCCESS", "TEMPORARY_FAILURE", "PERMANENT_FAILURE", "INSUFFICIENT_FUNDS", "ABANDONED", "REPEATED_FAILURE"],
        weights=[35, 20, 10, 10, 10, 15],
        k=1,
    )[0]

    if scenario == "SUCCESS":
        status = "SUCCESS"
        reason = ""
        retry_count = 0
        checkout_attempted = True
    elif scenario == "TEMPORARY_FAILURE":
        status = "FAILED"
        reason = random.choice(["NETWORK_ERROR", "BANK_TIMEOUT", "GATEWAY_TIMEOUT", "TEMPORARY_BANK_DECLINE"])
        retry_count = random.randint(0, 1)
        checkout_attempted = True
    elif scenario == "INSUFFICIENT_FUNDS":
        status = "FAILED"
        reason = "INSUFFICIENT_FUNDS"
        retry_count = random.randint(0, 2)
        checkout_attempted = True
    elif scenario == "PERMANENT_FAILURE":
        status = "FAILED"
        reason = random.choice(["CARD_EXPIRED", "PAYMENT_DECLINED", "FRAUD_DETECTED", "AUTHENTICATION_REQUIRED", "INVALID_PAYMENT_DETAILS"])
        retry_count = random.randint(0, 1)
        checkout_attempted = True
    elif scenario == "ABANDONED":
        status = "ABANDONED"
        reason = "CHECKOUT_ABANDONED"
        retry_count = 0
        checkout_attempted = True
    else:
        status = "FAILED"
        reason = random.choice([
            "NETWORK_ERROR", "BANK_TIMEOUT", "GATEWAY_TIMEOUT", "TEMPORARY_BANK_DECLINE",
            "INSUFFICIENT_FUNDS", "CARD_EXPIRED", "PAYMENT_DECLINED", "FRAUD_DETECTED",
            "AUTHENTICATION_REQUIRED", "INVALID_PAYMENT_DETAILS"
        ])
        retry_count = random.randint(2, 4)
        checkout_attempted = True

    rows.append([
        f"P-{i:05d}",
        f"M-{random.randint(1, 10):03d}",
        f"C-{random.randint(1, 100):04d}",
        amount,
        "INR",
        random.choice(payment_methods),
        status,
        reason,
        created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        retry_count,
        checkout_attempted,
    ])

with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"GENERATED {len(rows)} payment records.")
print(f"Saved to: {OUTPUT_FILE}")