from typing import Annotated

import json
import datetime
from loguru import logger
import random
import httpx
from fastapi import APIRouter, Security, HTTPException, status, Body, Response
from auth import check_token
import db
import auth


def generate_code():
    return random.randint(100000, 999999)

router = APIRouter(prefix="/verification")
@router.post("/send-code")
async def send_verification_code(response: Response, phone: str = Body(..., embed=True)):
    phone, role = phone.split("-") if "-" in phone else (phone, None)
    verification_code = generate_code()
    try:
        db.execute_query("INSERT INTO verification_codes (phone, code) VALUES (%s, %s) ON DUPLICATE KEY UPDATE code = %s, timestamp = CURRENT_TIMESTAMP", (phone, verification_code, verification_code))
        db.connection.commit()
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    logger.debug(f"Verification code sent to {phone}: {verification_code}")
    return {"result": True}


@router.post("/verify-code")
async def verify_code(response: Response, phone: str = Body(..., embed=True), code: int = Body(..., embed=True)):
    phone, role = phone.split("-")
    result = db.fetch_one("SELECT timestamp FROM verification_codes WHERE phone = %s AND code = %s", (phone, code))
    if result and (datetime.datetime.now() - result[0]).total_seconds() < 120:
        return {"result": True, 'token': await auth.generate_phone_token("-".join([phone, role]))}
    response.status_code = status.HTTP_403_FORBIDDEN
    return {"result": False}