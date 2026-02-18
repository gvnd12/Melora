from fastapi import FastAPI

from app.api import auth_router, user_router, song_router

app = FastAPI(title="Songs", docs_url="/")

app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=song_router)