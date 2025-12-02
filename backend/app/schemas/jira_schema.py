from pydantic import BaseModel
from typing import Any, Optional

class JiraResponse(BaseModel):
    ticket_id: str
    project: Optional[str]
    summary: Optional[str]
    description: Any
    raw_description: Any
    acceptance_criteria: Optional[Any]