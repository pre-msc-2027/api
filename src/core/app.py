import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager
from src.routes import rules, scans, repos
from src.routes.repo_github import router as repo_router
from src.core.database import init_db
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield 

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(rules.router)
app.include_router(scans.router)
app.include_router(repos.router)

def start():
    uvicorn.run(app,host= '0.0.0.0',  port= 8001)
    print('api qui marche ')
