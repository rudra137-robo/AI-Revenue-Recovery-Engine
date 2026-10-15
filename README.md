# ⚡ Razorpay AI Revenue Recovery Engine

> **Razorpay AI Buildathon Submission — Track 3: AI Revenue Recovery**  
> An autonomous, agentic revenue recovery system that diagnoses payment failures, computes financial recovery probability, and deploys hyper-personalized AI interventions to salvage lost transactions.

---

## 🚀 The Problem
Merchant payment flows face constant friction: network timeouts, bank drops, insufficient funds, expired cards, and abandoned checkouts. Millions of rupees in legitimate revenue are lost daily because standard retry logic is static and impersonal.

## 💡 The Solution
Our AI Revenue Recovery Engine introduces a 3-tier intelligent architecture:
1. **Failure Diagnosis Engine:** Instantly categorizes root causes (`INSUFFICIENT_FUNDS`, `CARD_EXPIRED`, `NETWORK_ERROR`, etc.) from transactional metadata.
2. **Deterministic & Probabilistic Heuristics:** Calculates expected recovery amounts and selects the optimal intervention (Smart Retry, Pay-Later nudge, Dynamic Discount, or Alternative Payment Link).
3. **Generative LLM Agent:** Uses LiteLLM to draft conversion-optimized, hyper-personalized WhatsApp/SMS recovery messages tailored to each customer.

---

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Pydantic, Uvicorn
* **Data Processing:** Pandas, CSV-based batch simulation
* **AI / LLM Layer:** LiteLLM (OpenAI / multi-provider integration)
* **Frontend Dashboard:** Tailwind CSS, responsive single-page metrics viewer

---

## 📊 Performance & Metrics (Synthetic Batch Simulation)
* **Total Records Processed:** 100 Transactions
* **Total Failed Volume:** ₹4,29,429 INR
* **Projected AI Recovery:** ₹2,53,535.65 INR
* **Projected Recovery Rate:** **59.04%** efficiency across automated workflows.

---

## ⚙️ Quick Start Guide

### 1. Clone & Set Up Environment
```powershell
git clone [https://github.com/your-username/AI-Revenue-Recovery-Engine.git](https://github.com/your-username/AI-Revenue-Recovery-Engine.git)
cd AI-Revenue-Recovery-Engine

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pandas pydantic python-dotenv litellm