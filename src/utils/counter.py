import hashlib
from src.models.counter import Counter
from beanie.operators import Inc

async def get_next_sequence(key: str) -> str:
    counter = await Counter.find_one(Counter.key == key)

    if counter:
        await counter.set(Inc({Counter.count: 1}))
        await counter.fetch() 
    else:
        counter = Counter(key=key, count=1)
        await counter.insert()

    raw_value = f"{key}:{counter.count}"
    hashed = hashlib.sha256(raw_value.encode()).hexdigest()

    return hashed