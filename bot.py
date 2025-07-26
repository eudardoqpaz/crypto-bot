import os
import time
import logging
import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Variables de entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

# Inicializar el bot
bot = Bot(token=BOT_TOKEN)

def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana,binancecoin,cardano",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = [
        f"BTC: ${data['bitcoin']['usd']}",
        f"ETH: ${data['ethereum']['usd']}",
        f"SOL: ${data['solana']['usd']}",
        f"BNB: ${data['binancecoin']['usd']}",
        f"ADA: ${data['cardano']['usd']}"
    ]
    return "\n".join(prices)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot activo. Escribe 'Actualizame'.")

def handle_message(update, context):
    if update.message.text.lower() == "actualizame":
        prices = get_crypto_data()
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"🟢 Precios actuales:\n{prices}")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
