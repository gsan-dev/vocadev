from aiohttp import web
import discord
import os
import logging

logger = logging.getLogger('discord')

class WebServer:
    def __init__(self, bot):
        self.bot = bot
        self.app = web.Application()
        # Escuchar peticiones POST en /webhook
        self.app.router.add_post('/webhook', self.handle_webhook)
        # Escuchar peticiones GET en la raiz para un checkeo simple de salud
        self.app.router.add_get('/', self.handle_health)
        self.port = int(os.getenv("WEBHOOK_PORT", 15830))

    async def handle_health(self, request):
        return web.Response(text="El servidor de webhook está funcionando.")

    async def handle_webhook(self, request):
        try:
            data = await request.json()
            # Enviar el json a procesar asincronamente
            self.bot.loop.create_task(self.process_kuma_alert(data))
            return web.Response(text="Procesado", status=200)
        except Exception as e:
            logger.error(f"Error parseando webhook JSON: {e}")
            return web.Response(text="Bad Request", status=400)

    async def process_kuma_alert(self, data):
        target_user_id = int(os.getenv("TARGET_USER_ID", 0))
        if target_user_id == 0:
            logger.warning("TARGET_USER_ID no configurado, no se puede enviar mensaje.")
            return

        user = self.bot.get_user(target_user_id)
        if not user:
            try:
                user = await self.bot.fetch_user(target_user_id)
            except Exception as e:
                logger.error(f"No se pudo encontrar al usuario destino: {e}")
                return

        # Uptime Kuma payload típico:
        monitor_name = data.get("monitor", {}).get("name", "Servicio Desconocido")
        # El status suele venir bajo "heartbeat", status=1 (UP), status=0 (DOWN) o status=2 (PENDING)
        status = data.get("heartbeat", {}).get("status", 0) 
        msg = data.get("msg", "Sin información adicional")
        heartbeat_ping = data.get("heartbeat", {}).get("ping", "N/A")

        if status == 1:
            color = discord.Color.green()
            status_text = "💚 RECUPERADO / ONLINE"
        elif status == 0:
            color = discord.Color.red()
            status_text = "💔 CAÍDO / OFFLINE"
        else:
            color = discord.Color.orange()
            status_text = "⚠️ PENDIENTE / ESTADO DESCONOCIDO"

        embed = discord.Embed(
            title=f"Notificación de Uptime Kuma",
            description=f"**Servicio:** `{monitor_name}`\n**Mensaje:** {msg}",
            color=color
        )
        embed.add_field(name="Estado", value=status_text, inline=True)
        embed.add_field(name="Ping", value=f"{heartbeat_ping} ms", inline=True)
        embed.set_footer(text="Homelab Discord Bot")

        try:
            await user.send(embed=embed)
        except Exception as e:
            logger.error(f"Error al enviar DM al usuario: {e}")

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        logger.info(f"AIOHTTP WebServer está escuchando en el puerto {self.port}")
