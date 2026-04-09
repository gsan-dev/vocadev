import discord
from discord import app_commands
from discord.ext import commands

class StatusCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Muestra el estado interno del bot y de sus subsistemas")
    async def status_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Estado del Sistema Homelab",
            description="El bot de monitoreo y su servidor API de la red interna se encuentran activos y a la escucha de nuevas interacciones.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Latencia de Conexión", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Mapeo de Módulos (Cogs)", value=f"{len(self.bot.cogs)} cargados", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(StatusCommand(bot))
