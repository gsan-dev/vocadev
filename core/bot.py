import discord
from discord.ext import commands
import os
import logging
from core.webserver import WebServer
from pathlib import Path

logger = logging.getLogger('discord')

class UptimeKumaBot(commands.Bot):
    def __init__(self):
        # Configuramos los intents (solo requerimos default para slash commands y DMs)
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        
        # Instanciar el servidor web aiohttp
        self.webserver = WebServer(self)

    async def setup_hook(self):
        """
        Este método se ejecuta un instante antes de que el bot se conecte a Discord.
        Es ideal para cargar extensiones (cogs) y tareas en background.
        """
        logger.info("Cargando Cogs recursivamente...")
        
        cogs_dir = Path(__file__).resolve().parent.parent / 'cogs'
        
        if cogs_dir.exists():
            for filepath in cogs_dir.rglob("*.py"):
                # Ignorar archivos que empiecen por __ (como __init__.py)
                if filepath.name.startswith("__"):
                    continue
                
                # Convertir la ruta del sistema a un string de modulo (ej. cogs.commands.system.ping)
                relative_path = filepath.relative_to(cogs_dir.parent)
                module_str = ".".join(relative_path.with_suffix("").parts)
                
                try:
                    await self.load_extension(module_str)
                    logger.info(f"Módulo cargado exitosamente: {module_str}")
                except Exception as e:
                    logger.error(f"Fallo al cargar el módulo {module_str}: {e}")
        
        logger.info("Sincronizando Slash Commands...")
        await self.tree.sync()

        logger.info("Iniciando el servidor web de Webhooks...")
        self.loop.create_task(self.webserver.start())
