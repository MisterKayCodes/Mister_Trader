from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.export_service import export_trades_to_csv, get_export_filename

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/trades/csv")
def export_trades_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    csv_data = export_trades_to_csv(db, current_user.id)
    filename = get_export_filename(current_user.id)
    
    return StreamingResponse(
        csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
