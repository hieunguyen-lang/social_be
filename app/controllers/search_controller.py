from fastapi import APIRouter, Depends, HTTPException, status,Query,Response,Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..redis_client import get_redis
from ..models import User, UserRole
from ..schemas.hoadon_schemas import HoaDonOut,HoaDonUpdate,HoaDonCreate
from ..schemas.hoadon_dien_schemas import HoaDonDienCreate,HoaDonDienUpdate
from ..schemas.search_schemas import CrawlerPostItem
from ..auth import get_current_active_user, get_current_admin_user
from ..services import search_service
from typing import Any
from app.auth_permission import require_permission
import httpx
from urllib.parse import unquote
router = APIRouter()



#Hóa đơn điện

@router.get("/",response_model=List[CrawlerPostItem], summary="Tìm kiếm bài viết trên mạng xã hội")
async def searchSocial(
    request: Request,  
    keyword: str = Query(None, description="Tìm kiếm keyword"),

    # current_user: User = Depends(get_current_active_user),
    # perm: bool = Depends(require_permission("bill:view"))
):  
    client_ip = request.client.host
    filters = {
        "keyword": keyword,
        "client_ip": client_ip
    }
    # Loại bỏ các giá trị None khỏi filters
    filters = {k: v for k, v in filters.items() if v is not None}
    return await search_service.searchSocial(
        filters=filters,
    )

@router.get("/proxy")
async def proxy_image(url: str = Query(...)):
    # Decode URL nếu bị encode
    url = unquote(url)

    # Request đến IG
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "image/jpeg")

        # Nếu file .heic mà trả về JPEG → đổi tên file
        if url.endswith(".heic") and content_type == "image/jpeg":
            content_disposition = 'inline; filename="image.jpg"'
        else:
            content_disposition = 'inline'

        return Response(
            content=resp.content,
            media_type=content_type,
            headers={
                "Content-Disposition": content_disposition
            }
        )
router = router