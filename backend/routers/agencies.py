from typing import Annotated
from pydantic import BaseModel

import json
from loguru import logger
from uuid import uuid4
import httpx
from fastapi import APIRouter, Security, HTTPException, status, Body, Response, Header, Depends
from auth import check_token
import db
import auth
from hashlib import sha256


router = APIRouter(prefix="/agency")


class Agency(BaseModel):
    name: str | None = None
    phone: str | None = None
    city: str | None = None
    employees_count: str | None = None
    admin_firstname: str | None = None
    admin_lastname: str | None = None
    admin_phone: str | None = None
    admin_password: str | None = None


def password_hash(password: str) -> str:
    return sha256(password.encode()).hexdigest()


@router.post("/register")
async def register(response: Response, agency: Agency = Body(...), user_info: dict = Depends(check_token)):
    phone = user_info['phone']
    if not phone:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": False, "message": "Invalid token"}
    # check if phone is already registered
    result = db.fetch_one("SELECT * FROM agencies WHERE admin_phone = %s", (agency.admin_phone,))
    if result:
        response.status_code = status.HTTP_409_CONFLICT
        return {"result": False, "message": "Phone number is already registered"}

    try:
        db.execute_query("INSERT INTO agencies (name, phone, city, employees_count, admin_firstname, admin_lastname, admin_phone, admin_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (agency.name, agency.phone, agency.city, agency.employees_count, agency.admin_firstname, agency.admin_lastname, phone, password_hash(agency.admin_password)))
        db.connection.commit()
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(e)
        return {"result": False, "message": "Internal server error"}
    return {"result": True}


@router.post("/login")
async def login(response: Response, phone: str = Body(..., embed=True), password: str = Body(..., embed=True)):
    result = db.fetch_one("SELECT * FROM agencies WHERE admin_phone = %s AND admin_password = %s", (phone.split("-")[0], password_hash(password)))
    if not result:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": False, "message": "Invalid credentials"}
    return {"result": True, "token": await auth.generate_phone_token(phone)}

@router.get("/info/{agency_id}")
async def get_agency(agency_id: int):
    result = db.fetch_one("SELECT name, phone, city, employees_count, admin_firstname, admin_lastname, admin_phone FROM agencies WHERE id = %s", (agency_id,))
    if not result:
        return {"result": False, "message": "Agency not found"}
    return {
        "result": True,
        "agency": {
            "name": result[0],
            "phone": result[1],
            "city": result[2],
            "employees_count": result[3],
            "admin_firstname": result[4],
            "admin_lastname": result[5],
            "admin_phone": result[6]
        }

    }