# bot.py
import telebot
from config import TOKEN
from handlers import BotHandlers

def main():
    bot = telebot.TeleBot(TOKEN)
    handlers = BotHandlers(bot)
    bot.infinity_polling()

if __name__ == "__main__":
    main()
