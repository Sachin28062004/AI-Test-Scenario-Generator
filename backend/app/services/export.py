import os
from datetime import datetime
from app.database import crud

EXPORT_DIR = os.getenv("EXPORT_DIR", "/app/exports")


def ensure_export_dir():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    return EXPORT_DIR


def save_scenarios_to_excel(batch_id: str, scenarios: list, db_session):
    """Save scenarios to Excel. batch_id is 'manual' or a custom identifier."""
    ensure_export_dir()
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{batch_id}_scenarios_{timestamp}.xlsx"
    filepath = os.path.join(EXPORT_DIR, filename)

    from openpyxl import Workbook
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

    rec = crud.save_export_record(db_session, batch_id, filename, filepath)
    return {"filename": filename, "filepath": filepath, "record_id": rec.id}
