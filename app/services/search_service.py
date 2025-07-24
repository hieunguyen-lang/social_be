import requests
import re
import random
import uuid
from lxml import html
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import cast, INT
from ..models.hoa_don_models import HoaDon
from ..models.hoa_don_momo_model import HoaDonDien
from ..models.hoa_don_doiung_model import DoiUng
from ..schemas.hoadon_schemas import HoaDonOut,HoaDonUpdate,HoaDonCreate
from .. schemas.hoadon_dien_schemas import HoaDonDienOut
from .. schemas.doiung_schemas import DoiUngOut
from ..models import User, UserRole, hoa_don_models
from ..auth import verify_password, get_password_hash
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from collections import defaultdict
from typing import List, Dict
from sqlalchemy import asc ,desc
from io import BytesIO
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from ..helpers import helper, request_get_data
from ..schemas.search_schemas import SearchPostOut
def send_alert(webhook_url,username,content):
        
        data = {
            "content": content,
            "username": username
        }
        response = requests.post(webhook_url, json=data)
async def searchSocial(filters):
    try:
        result_instagram, status_instagram = await request_get_data.get_request_data_instagram(filters.get("keyword"))
    except Exception as e:
        result_instagram=[]
        print(f"[ERORR] Error fetching Instagram data {str(e)}")
        status_instagram= "Error fetching Instagram data"
    try:
        result_threads, status_threads = await request_get_data.get_request_data_threads(filters.get("keyword"))
    except:
        result_threads = []
        status_threads= "Error fetching Threads"
    try:
        result_x, status_x = await request_get_data.get_request_data_x(filters.get("keyword"))
    except:
        result_x = []
        status_x= "Error fetching X"
    try:
        result_tiktok, status_tiktok = await request_get_data.get_request_data_tiktok(filters.get("keyword"))
    except:
        result_tiktok = []
        status_tiktok= "Error fetching tiktok data"
    try:
        result_tumblr, status_tumblr = await request_get_data.get_request_data_tumblr(filters.get("keyword"))  
    except:
        result_tumblr = []
        status_tumblr= "Error fetching tumblr data"

    try:
        result_linkedin, status_linkedin = await request_get_data.get_request_data_linkedin(filters.get("keyword"))  
    except:
        result_linkedin = []
        status_linkedin= "Error fetching linkedin data"
    try:
        result_fb_watch, status_fb_watch = await request_get_data.get_request_data_watchfb(filters.get("keyword"))  
    except:
        result_fb_watch = []
        status_fb_watch= "Error fetching linkedin data"
    combined = result_instagram + result_threads + result_x + result_tiktok +result_tumblr +result_linkedin + result_fb_watch

    combined.sort(key=lambda x: x.post_created_timestamp, reverse=True)

    username ="Social Crawler"
    content = (
        "📢 Social Crawler health logs!\n"
        f"client_ip: {filters.get('client_ip')}\n"
        f"===========================================\n"
        f"Result_instagram: {len(result_instagram)}\n"
        f"Status_instagram: {status_instagram}\n"
        f"===========================================\n"
        f"Result_threads: {len(result_threads)}\n"
        f"Status_threads: {status_threads}\n"
        f"===========================================\n"
        f"Result_x: {len(result_x)}\n"
        f"Status_x: {status_x}\n"
        f"===========================================\n"
        f"Result_tiktok: {len(result_tiktok)}\n"
        f"Status_tiktok: {status_tiktok}\n"
        f"===========================================\n"
        f"Result_tumblr: {len(result_tumblr)}\n"
        f"Status_tumblr: {status_tumblr}\n"
        f"===========================================\n"
        f"Result_linkedin: {len(result_linkedin)}\n"
        f"Status_linkedin: {status_linkedin}\n"
        f"===========================================\n"
        f"Result_fb_watch: {len(result_fb_watch)}\n"
        f"Status_fb_watch: {status_fb_watch}\n"
        f"Total: {len(combined)}"
    )
    send_alert("https://discord.com/api/webhooks/1396778930232627220/rjLenkP2J1G3MaO7rFY-Y5_8KlMY0DU6sfW8oxNoyony18oFopVK2RUsgOQWuIvzCKyb",username,content)
    return combined

