from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import database
from app.services.test_generator import generate_scenarios_from_description
from app.services.export import save_scenarios_to_excel
from app.database import crud
from app.routers.auth import get_current_user
from app.database.models import User

router = APIRouter(prefix="/api/ai", tags=["ai"])


class GenerateRequest(BaseModel):
    description: str
    title: str = ""


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate")
async def generate_scenarios(
    payload: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate test scenarios from user-provided description (no Jira).
    Requires JWT auth.
    """
    if not payload.description or not payload.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    try:
        parsed = generate_scenarios_from_description(
            payload.description,
            payload.title or "",
            db
        )
        scenarios = parsed.get("scenarios", [])

        batch_id = "manual"
        export_meta = save_scenarios_to_excel(batch_id, scenarios, db)

        return {
            "enhanced_description": parsed.get("enhanced_description"),
            "scenarios": scenarios,
            "scenarios_count": len(scenarios),
            "export": export_meta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exports")
def list_exports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recs = crud.list_exports(db)
    return [
        {"id": r.id, "ticket_id": r.ticket_id, "filename": r.filename, "filepath": r.filepath, "generated_at": r.generated_at}
        for r in recs
    ]
