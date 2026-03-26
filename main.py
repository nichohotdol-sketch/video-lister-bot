# ===============================
# BOT VIP 24/7 (FLASK + SELF PING)
# ===============================

import os
import asyncio
import random
import pytz
from datetime import datetime, time
from telethon import TelegramClient
from flask import Flask
from threading import Thread
import requests
import time as t

# Evita erro caso 'imghdr' não exista (Python 3.13+)
try:
    import imghdr
except ModuleNotFoundError:
    pass

# -------------------------------
# CONFIGURAÇÕES
# -------------------------------

API_ID = int(os.environ.get("API_ID", 38125495))
API_HASH = os.environ.get("API_HASH", "3bff4dc410d55586b56b4341d824cf93")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "SEU_TOKEN_AQUI")

REPLIT_URL = os.environ.get(
    "REPLIT_URL",
    "https://video-lister-bot--nichohotdol.replit.app/"  # atenção à barra final
)

STORAGE_CHANNEL = os.environ.get("STORAGE_CHANNEL", "@hospedag")
PREVIAS_CHAT = int(os.environ.get("PREVIAS_CHAT", -1003689135136))
LEGEND = "😈O VIP TA ON PEGUE SEU ACESSO AO VIP AGORA\n\nCHAMA 👇\n@hotmetflixs_bot"

# -------------------------------
# FLASK (ANTI-SLEEP)
# -------------------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot rodando 24/7 😎"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()

# -------------------------------
# SELF PING (MANTÉM ONLINE)
# -------------------------------

def self_ping():
    while True:
        try:
            requests.get(REPLIT_URL, verify=False)
            print("Ping enviado para manter bot acordado")
        except Exception as e:
            print("Erro no ping:", e)
        t.sleep(280)  # ping a cada 4min40s

Thread(target=self_ping).start()

# -------------------------------
# TELEGRAM CLIENT (USANDO BOT TOKEN)
# -------------------------------

client = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def dentro_do_horario():
    tz = pytz.timezone("America/Bahia")
    agora = datetime.now(tz).time()
    if time(18, 0) <= agora <= time(23, 59):
        return 20
    else:
        return 30

async def main():
    print("Bot iniciado!")

    # 🔥 Delay para garantir Flask e pings ativos
    await asyncio.sleep(5)

    # Busca vídeos no canal de armazenamento
    videos = []
    async for msg in client.iter_messages(STORAGE_CHANNEL):
        if msg.video:
            videos.append(msg.id)

    print(f"Total de vídeos encontrados: {len(videos)}")
    if not videos:
        return

    while True:
        random.shuffle(videos)
        for video_id in videos:
            try:
                arquivo = f"video_{video_id}.mp4"
                msg = await client.get_messages(STORAGE_CHANNEL, ids=video_id)
                await msg.download_media(file=arquivo)
                await client.send_file(PREVIAS_CHAT, arquivo, caption=LEGEND)
                os.remove(arquivo)

                intervalo = dentro_do_horario()
                delay = random.randint(5, 30)
                total = intervalo * 60 + delay
                print(f"Enviado vídeo {video_id}. Próximo em {total//60} min")
                await asyncio.sleep(total)

            except Exception as e:
                print(f"Erro ao enviar vídeo {video_id}: {e}")
                continue

# -------------------------------
# INICIAR BOT
# -------------------------------

if __name__ == "__main__":
    asyncio.run(main())
