import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#User files
from routers.listings import router as listings_router
from dotenv import load_dotenv

load_dotenv()

ALLOWED_ORIGINS = os.get_env("VITE_API_URL", "http://localhost:5173")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings_router)
