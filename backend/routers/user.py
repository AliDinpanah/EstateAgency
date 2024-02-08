from typing import Annotated
from pydantic import BaseModel

import json
import datetime
from loguru import logger
import random
import httpx
from fastapi import APIRouter, Security, HTTPException, status, Body, Response, Header, Depends
from auth import check_token
import db
import auth
from hashlib import sha256

class User(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

router = APIRouter(prefix="/user")

def password_hash(password: str) -> str:
    return sha256(password.encode()).hexdigest()
    

@router.post("/register")
async def register(response: Response, user_info: dict = Depends(check_token)):
    phone = user_info["phone"]
    result = db.fetch_one("SELECT * FROM users WHERE phone = %s", (phone,))
    if result:
        response.status_code = status.HTTP_409_CONFLICT
        return {"result": False, "message": "Phone number is already registered"}

    try:
        db.execute_query("INSERT INTO users (phone) VALUES (%s)", (phone,))
        db.connection.commit()
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"result": False, "message": "Internal server error"}
    return {"result": True}

@router.put("/update")
async def update(response: Response, user: User = Body(...), user_info: dict = Depends(check_token)):
    phone = user_info["phone"]
    try:
        db.execute_query("UPDATE users SET email = %s, first_name = %s, last_name = %s WHERE phone = %s", (user.email, user.first_name, user.last_name, phone))
        if user.password:
            db.execute_query("UPDATE users SET password = %s WHERE phone = %s", (password_hash(user.password), phone))
        db.connection.commit()
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"result": False, "message": "Internal server error"}
    return {"result": True}

@router.get("/me")
async def get(response: Response, user_info: dict = Depends(check_token)):
    phone = user_info["phone"]
    result = db.fetch_one("SELECT email, first_name, last_name FROM users WHERE phone = %s", (phone,))
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": False, "message": "User not found"}
    return {"result": True, "user": {"email": result[0], "first_name": result[1], "last_name": result[2]}}

@router.post("/login")
async def login(response: Response, phone: str = Body(..., embed=True), password: str = Body(..., embed=True)):
    result = db.fetch_one("SELECT * FROM users WHERE phone = %s AND password = %s", (phone.split("-")[0], password_hash(password)))
    if not result:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": False, "message": "Phone number or password is incorrect"}
    return {"result": True, "token": await auth.generate_phone_token(phone)}