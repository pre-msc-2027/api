from models.counter import Counter
from beanie.operators import Inc

async def get_next_sequence(key: str) -> int:
    counter = await Counter.find_one(Counter.key == key)

    if counter:
        await counter.set(Inc({Counter.count: 1}))
        await counter.fetch() 
    else:
        counter = Counter(key=key, count=1)
        await counter.insert()

    return counter.count