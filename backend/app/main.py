from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import jira, settings, ai_routes, export_routes
from app.database import models
from app.database import database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(
    title="AI Test Scenario Generator Backend",
    version="1.0.0"
)

app.include_router(jira.router)
app.include_router(settings.router)
app.include_router(ai_routes.router)
app.include_router(export_routes.router)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running!"}