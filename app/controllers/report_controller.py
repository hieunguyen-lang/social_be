from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date
from typing import List, Literal
from typing import List
from ..database import get_db
from ..models import User, UserRole
from ..schemas.report_schemas import CommissionBySenderOut,HoaDonCalendarEvent
from ..auth import get_current_active_user, get_current_admin_user
from ..services import report_service
from typing import Any
from app.auth_permission import require_permission
router = APIRouter()




@router.get("/commission-by-sender", response_model=List[CommissionBySenderOut])
async def commission_by_sender(
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    perm: bool = Depends(require_permission("report:commission"))
):
    # Truy vấn và group theo người gửi
    return await report_service.commission_by_sender(from_date=from_date, to_date=to_date, db=db, current_user=current_user)

@router.get("/den-han-ket-toan", response_model=List[HoaDonCalendarEvent])
async def get_hoa_don_den_han_ket_toan(
    from_date: str = Query(..., alias="from"),
    to_date: str = Query(..., alias="to"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    perm: bool = Depends(require_permission("report:calendar"))
):
    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="Sai định dạng ngày (yyyy-mm-dd)")
    return await report_service.get_hoa_don_den_han_ket_toan(from_dt=from_dt, to_dt=to_dt, db=db, current_user=current_user)
    