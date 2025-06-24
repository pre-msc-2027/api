from fastapi import FastAPI
from src.routes import rules 

app = FastAPI()

app.include_router(rules.router)
