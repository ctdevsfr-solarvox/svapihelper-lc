import asyncio


class SVScheduler:
    def __init__(self):
        self.tasks = []

    def every(self, seconds: int):
        def wrapper(func):
            async def loop():
                while True:
                    await func()
                    await asyncio.sleep(seconds)
            self.tasks.append(loop())
            return func
        return wrapper

    async def start_all(self):
        await asyncio.gather(*self.tasks)
