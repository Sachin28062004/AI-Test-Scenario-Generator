from fastapi import FastAPI
from app.routers import jira, ai, export, history, settings_api

app = FastAPI(
    title="AI Test Scenario Generator Backend",
    version="1.0.0"
)

app.include_router(jira.router)
app.include_router(ai.router)
app.include_router(export.router)
app.include_router(history.router)
app.include_router(settings_api.router)

@app.get("/")
def root():
    return {"message": "Backend running!"}