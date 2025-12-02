# AI Test Scenario Generator

An AI-driven tool that:
- Fetches Jira stories using Jira API
- Enhances descriptions using Gemini Pro (via LangChain)
- Generates test scenarios (Frontend + Backend + DB)
- Allows editing scenarios in UI
- Exports PDF and Excel
- Maintains history
- Supports user settings for API keys

## 🛠 Tech Stack

### Backend
- Python (FastAPI)
- LangChain + Gemini Pro
- SQLAlchemy + SQLite
- ReportLab (PDF)
- openpyxl (Excel)

### Frontend
- Next.js
- Tailwind CSS
- Zustand
- Axios

### DevOps
- Docker
- Docker Compose

---

## 🚀 Setup

```bash
git clone <repo-url>
cd ai-test-scenario-generator

docker compose up --build
