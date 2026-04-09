import discord
from discord import app_commands
from discord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Comprueba si el bot está respondiendo")
    async def ping_command(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong! Latencia del ping bot: {round(self.bot.latency * 1000)}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
