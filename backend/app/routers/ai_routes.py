from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import database
from app.services.jira_client import JiraClient
from app.services.test_generator import enhance_description_and_generate_scenarios
from app.services.export import save_scenarios_to_excel
from app.database import crud
from typing import Dict, Any
from pydantic import BaseModel
import os
import json
import re

router = APIRouter(prefix="/api/ai", tags=["ai"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def safe_to_dict(data: [Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(data, dict):
        return data

    if hasattr(data, 'model_dump'):
        return data.model_dump()

    if hasattr(data, 'dict'):
        return data.dict()

    try:
        return json.loads(json.dumps(data, default=str))
    except Exception:
        return {"error": "Failed to convert Jira data object to dictionary."}

@router.post("/generate/{ticket_id}")
async def generate_for_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """
    Fetch ticket using stored Jira creds -> call Gemini -> save excel -> return metadata
    """
    try:
        jira_client = JiraClient(db)
        jira_data_object = jira_client.fetch_ticket(ticket_id)
        jira_data = safe_to_dict(jira_data_object)

        parsed = enhance_description_and_generate_scenarios(jira_data, db)
        # parsed expected to be a dict with enhanced_description & scenarios array
        scenarios = parsed.get("scenarios", [])

        export_meta = save_scenarios_to_excel(ticket_id, scenarios, db)
        return {
            "enhanced_description": parsed.get("enhanced_description"),
            "scenarios_count": len(scenarios),
            "export": export_meta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exports")
def list_exports(db: Session = Depends(get_db)):
    recs = crud.list_exports(db)
    return [{"id": r.id, "ticket_id": r.ticket_id, "filename": r.filename, "filepath": r.filepath, "generated_at": r.generated_at} for r in recs]
