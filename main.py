import asyncio
import os
from dotenv import load_dotenv
from core.bot import UptimeKumaBot

async def main():
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN no encontrado en el entorno o .env")
        return

    # Iniciar la instancia de nuestro bot
    bot = UptimeKumaBot()
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
