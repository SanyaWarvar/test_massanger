from fastapi import FastAPI
from src.auth.routers import router as auth_router
app = FastAPI(
    title="cool messanger"
)

app.include_router(auth_router)