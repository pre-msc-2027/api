import uvicorn
from fastapi import FastAPI
from src.routes import rules 

app = FastAPI()

app.include_router(rules.router)

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)
#app.middleware('http')(jwt_middleware)

def start():
    uvicorn.run(app,host= '0.0.0.0',  port= 5000)
