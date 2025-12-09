import discord
import asyncio


class SVPresenceUpdater:
    def __init__(self, bot, api):
        self.bot = bot
        self.api = api
        self.running = False

    async def start(self, interval=10):
        if self.running:
            return
        self.running = True

        while True:
            async with self.api.session() as api:
                info = await api.get_server_info()

            activity = discord.Game(
                f"{info.player_count} players | {info.queue} queued"
            )
            await self.bot.change_presence(activity=activity)

            await asyncio.sleep(interval)
