import discord
from discord import app_commands
from .client import SVAPI
from .models import Player


class SVDiscord:
    def __init__(self, bot: discord.Client, api: SVAPI):
        self.bot = bot
        self.api = api
        self.tree = app_commands.CommandTree(bot)

        # Role syncing config
        self.department_roles = {}
        self.rank_roles = {}

    # -----------------------------------------------
    # Slash command decorator
    # -----------------------------------------------
    def slash_command(self, name: str, description: str):
        def wrapper(func):
            @self.tree.command(name=name, description=description)
            async def command_wrapper(interaction: discord.Interaction, user_id: int):
                async with self.api.session() as api:
                    result = await func(interaction, api, user_id)
                await interaction.response.send_message(result)
            return func
        return wrapper

    # -----------------------------------------------
    # Auto Role Syncing
    # -----------------------------------------------
    def set_department_role(self, department: str, role_id: int):
        self.department_roles[department] = role_id

    def set_rank_role(self, rank: str, role_id: int):
        self.rank_roles[rank] = role_id

    async def sync_roles(self, member: discord.Member, roblox_id: int):
        async with self.api.session() as api:
            player: Player = await api.get_player(roblox_id)

        updated_roles = []

        if player.team in self.department_roles:
            role = member.guild.get_role(self.department_roles[player.team])
            updated_roles.append(role)

        if player.rank in self.rank_roles:
            role = member.guild.get_role(self.rank_roles[player.rank])
            updated_roles.append(role)

        await member.edit(roles=updated_roles)

    # -----------------------------------------------
    # Register commands with Discord
    # -----------------------------------------------
    async def setup(self):
        await self.tree.sync()
