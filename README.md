# AI Test Scenario Generator
[App Link] : https://ai-test-scenario-generator.vercel.app/home

An AI-driven tool that:
- Accepts feature/requirement descriptions (paste or type)
- Enhances descriptions using Grok (xAI)
- Generates test scenarios (Frontend + Backend + DB)
- Allows editing scenarios in UI
- Exports CSV and Excel
- JWT-secured API

## 🛠 Tech Stack

### Backend
- Python (FastAPI)
- Grok (xAI) API
- JWT authentication
- SQLAlchemy + SQLite
- openpyxl (Excel)

### Frontend
- Angular
- Axios

### DevOps
- Docker
- Docker Compose

---

## 🚀 Setup

```bash
git clone <repo-url>
cd ai-test-scenario-generator
```

### Backend environment
Create `backend/.env`:
```
ENCRYPTION_KEY=<base64-key>
JWT_SECRET=<long-random-string-for-production>
```

### Run
```bash
docker compose up --build
```

### First use
1. Register a new account at `/login`
2. Sign in
3. Go to **Settings** and add your Grok (xAI) API key
4. Go to **Home**, paste a feature description, and generate scenarios
