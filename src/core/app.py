import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes import rules, scans, repos
from src.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield 

app = FastAPI(lifespan=lifespan)

app.include_router(rules.router)
app.include_router(scans.router)
app.include_router(repos.router)

def start():
    uvicorn.run(app,host= '0.0.0.0',  port= 8000)
