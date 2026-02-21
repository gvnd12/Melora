from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_router, song_router, user_router

app = FastAPI(title="Songs", docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=song_router)
