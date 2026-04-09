import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')

class ReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Sistema en Línea: Autenticado como {self.bot.user.name} (Client ID: {self.bot.user.id})')
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name="Servicios Homelab"
            )
        )

async def setup(bot):
    await bot.add_cog(ReadyEvent(bot))
