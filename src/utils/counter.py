import hashlib
import random

from src.models.counter import Counter
from beanie.operators import Inc

async def get_next_sequence(key: str) -> str:
    count = random.randint(1, 10000000)
    counter = Counter(key=key, counter=count)
    await counter.insert()

    raw_value = f"{key}:{counter.counter}"
    hashed = hashlib.sha256(raw_value.encode()).hexdigest()

    return hashed
