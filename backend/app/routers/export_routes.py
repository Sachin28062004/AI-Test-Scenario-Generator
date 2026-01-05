from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.database import database, crud
import os

from requests import Session

router = APIRouter(prefix="/api/exports", tags=["exports"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/download/{record_id}")
def download_export(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(crud.models.ExportRecord).filter(crud.models.ExportRecord.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Export not found")
    if not os.path.exists(rec.filepath):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(path=rec.filepath, filename=rec.filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
