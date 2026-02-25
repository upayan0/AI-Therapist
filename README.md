# 🧠 SafeSpace: Multi-Agent AI Mental Health Therapist

**SafeSpace** is an advanced, multi-agent AI ecosystem designed to provide empathetic mental health support, therapeutic guidance, and automated crisis intervention. By integrating high-performance LLM routing with specialized medical models, SafeSpace bridges the gap between digital companionship and real-world safety.

---

## 📸 System Showcase

### **User Experience**

> A serene, dark-themed interface built for focus, safety, and emotional expression.
 ![WhatsApp Image 2026-02-26 at 2 13 14 AM](https://github.com/user-attachments/assets/43cb67cb-d1e5-45d2-bd5e-6e067e1f4a78)

### **Intelligent Architecture**

> A high-level overview of the request-response pipeline and multi-model orchestration.
![architecture](https://github.com/user-attachments/assets/28e1e749-e696-4701-8524-854091bff44e)

### **Crisis Intervention**

> Demonstrating the automated emergency escalation protocol in action.
![emergency_call](https://github.com/user-attachments/assets/c05511bc-8446-4fb0-a07c-6afcfedff30d)

---

## ✨ Core Features

* **❤️ Clinical Empathy**: Utilizes the **MedGemma** model to deliver warm, psychologist-style responses that normalize emotions and provide practical guidance.
* **🤖 Multi-Agent Routing**: Employs **Llama-3.1-8b (via Groq)** to intelligently classify user intent into `CASUAL`, `EMOTIONAL`, or `THERAPIST_LOOKUP` categories.
* **🚨 Emergency Escalation**: A critical safety layer that detects high-risk keywords and triggers an automated voice call via **Twilio**.
* **🧠 Contextual Intelligence**: Maintains a conversation window of the last 10 messages with automated token trimming to ensure long-term coherence.
* **📍 Local Support**: Natural language parsing to help users identify nearby mental health professionals.

---

## 🛠️ Technical Stack

| Layer | Technology | Role |
| --- | --- | --- |
| **Frontend** | Streamlit | Responsive UI & Mood Tracking |
| **API Engine** | FastAPI | High-performance backend orchestration |
| **Routing LLM** | Groq (Llama 3.1) | Intent classification & Agent logic |
| **Clinical LLM** | Ollama (MedGemma) | Therapeutic response generation |
| **Safety Layer** | Twilio API | Automated emergency voice calls |

---

## 🚀 Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/upayan0/ai-therapist.git
cd SafeSpace

# Install dependencies
pip install -r requirements.txt

```

### 2. Configuration

Create a `config.py` (or set environment variables) with the following:

```python
GROQ_API_KEY = "your_groq_key"
TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_FROM_NUMBER = "+1234567890"
EMERGENCY_CONTACT = "+91XXXXXXXXXX"

```

### 3. Launch

**Start the Backend Engine:**

```bash
uvicorn backend.main:app --reload

```

**Start the Web Interface:**

```bash
streamlit run frontend/frontend.py

```

---

## 📂 Project Structure

```text
SafeSpace/
├── backend/
│   ├── main.py          # FastAPI Entry Point
│   ├── ai_agent.py      # Routing & Agent Logic
│   └── tools.py         # MedGemma & Twilio Integration
├── frontend/
│   └── frontend.py      # Streamlit UI
├── requirements.txt     # Dependency Management
└── .gitignore           # Secret protection

```

---

## ⚠️ Safety Disclaimer

**SafeSpace is an AI-powered supportive tool and is NOT a replacement for professional clinical therapy or emergency services.** The emergency call feature is a safety supplement and relies on third-party API availability.

---

**Would you like me to help you design a persistent SQL database schema to track user mood trends over time?**
