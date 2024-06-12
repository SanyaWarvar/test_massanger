from fastapi import FastAPI
from src.auth.routers import router as auth_router
from src.messanger.routers import router as ws_router
app = FastAPI(
    title="cool messanger"
)

app.include_router(auth_router)
app.include_router(ws_router)