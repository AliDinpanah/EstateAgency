from typing import Annotated
from pydantic import BaseModel

import json
from loguru import logger
from uuid import uuid4
import httpx
from fastapi import APIRouter, Security, HTTPException, status, Body, Response, Header, UploadFile, Depends, File
from fastapi.responses import HTMLResponse
from auth import check_token
import db
import auth

router = APIRouter(prefix="/files")

@router.post("/upload/")
async def upload_file(response: Response, file: UploadFile = File(...)):
    if file.content_type != "image/jpeg" and file.content_type != "image/png":
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"result": False, "message": "Invalid file type"}
    file.filename = f"{uuid4()}.{file.filename.split('.')[-1]}"
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"result": True, "filename": file.filename}

@router.get("/{file_name}")
async def get_file(file_name: str):
    image_bytes = open(f"uploads/{file_name}", "rb").read()
    return Response(content=image_bytes, media_type="image/jpeg" if file_name.endswith(".jpg") else "image/png")