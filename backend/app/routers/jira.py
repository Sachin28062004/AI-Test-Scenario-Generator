from fastapi import APIRouter, HTTPException
from app.services.jira_client import JiraClient
from app.schemas.jira_schema import JiraResponse


router = APIRouter(prefix="/api/jira", tags=["Jira"])

@router.get("/{ticket_id}", response_model=JiraResponse)
async def get_jira_ticket(ticket_id: str):
    try: 
        jira = JiraClient()
        data = jira.fetch_ticket(ticket_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))