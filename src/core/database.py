from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.models import Scan, Rule, Repo
import os
from dotenv import load_dotenv

from src.models.counter import Counter


async def init_db():
    load_dotenv()

    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DBNAME")

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]

    await init_beanie(database=db, document_models=[Scan, Rule, Repo, Counter])
