from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import routers.agencies
import routers.verification
import routers.user
import routers.uploads
import routers.ads


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.agencies.router)
app.include_router(routers.verification.router)
app.include_router(routers.user.router)
app.include_router(routers.uploads.router)
app.include_router(routers.ads.router)
