import os
from openpyxl import Workbook
from datetime import datetime
from app.database import crud

EXPORT_DIR = os.getenv("EXPORT_DIR", "/app/exports")

def ensure_export_dir():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    return EXPORT_DIR

def save_scenarios_to_excel(ticket_id: str, scenarios: list, db_session):
    ensure_export_dir()
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{ticket_id}_scenarios_{timestamp}.xlsx"
    filepath = os.path.join(EXPORT_DIR, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Test Scenarios"
    ws.append(["Scenario ID", "Type", "Title", "Steps", "Expected Result"])

    for s in scenarios:
        sid = s.get("id") or ""
        stype = s.get("type") or ""
        title = s.get("title") or ""
        steps = "\n".join(s.get("steps", [])) if isinstance(s.get("steps"), list) else (s.get("steps") or "")
        expected = s.get("expected_result") or ""
        ws.append([sid, stype, title, steps, expected])

    wb.save(filepath)

    # Save record in DB
    rec = crud.save_export_record(db_session, ticket_id, filename, filepath)
    return {"filename": filename, "filepath": filepath, "record_id": rec.id}
