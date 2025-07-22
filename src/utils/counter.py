import hashlib
from src.models.counter import Counter
from beanie.operators import Inc

async def get_next_sequence(key: str) -> str:
    counter = await Counter.find_one(Counter.key == key)

    if counter:
        counter = await Counter.find_one_and_update(
            Counter.key == key,
            Inc({Counter.counter: 1}),
            return_document=True
        )
    else:
        counter = Counter(key=key, counter=1)
        await counter.insert()

    raw_value = f"{key}:{counter.counter}"
    hashed = hashlib.sha256(raw_value.encode()).hexdigest()

    return hashed
