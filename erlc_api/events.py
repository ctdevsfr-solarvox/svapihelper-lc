class SVEventManager:
    def __init__(self):
        self.handlers = {}

    def on(self, event_name: str):
        def wrapper(func):
            self.handlers.setdefault(event_name, []).append(func)
            return func
        return wrapper

    async def dispatch(self, event_name: str, payload):
        if event_name in self.handlers:
            for func in self.handlers[event_name]:
                await func(payload)
