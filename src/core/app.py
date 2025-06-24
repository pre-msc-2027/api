from fastapi import FastAPI
from src.routes import rules
from src.user import router as user_router
from src.routes.repo import router as repo_router
app = FastAPI()

app.include_router(rules.router)

app.include_router(user_router, prefix="/user")
app.include_router(repo_router, prefix="/repo")
