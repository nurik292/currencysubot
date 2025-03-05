import os
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Загружаем токены из .env
load_dotenv()
BOT_TOKEN = os.getenv("7782389964:AAER1cF82oTsE2PO5yV3pcOaidlD2C5UQxY")
API_KEY = os.getenv("95ca9d801b47feaa90689aad")
BASE_URL = f"https://v6.exchangerate-api.com/v6/95ca9d801b47feaa90689aad/latest/USD"

# Валюты, которые поддерживаются
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY", "JPY"]

# Функция выбора валюты
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(cur, callback_data=f"from_{cur}")] for cur in CURRENCIES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите валюту, из которой хотите конвертировать:", reply_markup=reply_markup)

# Обработка выбора валюты
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    data = query.data.split("_")
    
    if data[0] == "from":
        context.user_data["from_currency"] = data[1]
        keyboard = [[InlineKeyboardButton(cur, callback_data=f"to_{cur}")] for cur in CURRENCIES]
        query.edit_message_text(text=f"Вы выбрали {data[1]}. Теперь выберите валюту для конвертации:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data[0] == "to":
        context.user_data["to_currency"] = data[1]
        query.edit_message_text(text=f"Вы выбрали {context.user_data['from_currency']} → {data[1]}. Введите сумму:")

# Обработка текста (сумма)
def text_handler(update: Update, context: CallbackContext):
    if "from_currency" not in context.user_data or "to_currency" not in context.user_data:
        update.message.reply_text("Сначала выберите валюты с помощью /start")
        return

    try:
        amount = float(update.message.text)
        from_currency = context.user_data["from_currency"]
        to_currency = context.user_data["to_currency"]
        
        response = requests.get(BASE_URL + from_currency)
        data = response.json()
        
        if "conversion_rates" not in data:
            update.message.reply_text("Ошибка при получении курса валют.")
            return
        
        rate = data["conversion_rates"].get(to_currency)
        if not rate:
            update.message.reply_text("Ошибка. Выбранная валюта не поддерживается.")
            return

        result = amount * rate
        update.message.reply_text(f"{amount} {from_currency} = {result:.2f} {to_currency}")
    
    except ValueError:
        update.message.reply_text("Введите корректное число.")

# Основная функция
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("convert", start))  # Повторный запуск
    dp.add_handler(CommandHandler("help", start))  # Инструкция
    dp.add_handler(CommandHandler("cancel", start))  # Сброс
    dp.add_handler(CommandHandler("reset", start))  # Сброс
    dp.add_handler(CommandHandler("menu", start))  # Перезапуск меню
    dp.add_handler(CommandHandler("back", start))  # Назад к выбору
    dp.add_handler(CommandHandler("currency", start))  # Выбор валют
    dp.add_handler(CommandHandler("restart", start))  # Перезапуск
    dp.add_handler(CommandHandler("startover", start))  # Начать заново
    dp.add_handler(CommandHandler("convertagain", start))  # Конвертация снова
    dp.add_handler(CommandHandler("tryagain", start))  # Попробовать снова
    dp.add_handler(CommandHandler("another", start))  # Выбрать другую валюту
    dp.add_handler(CommandHandler("new", start))  # Новая операция
    dp.add_handler(CommandHandler("change", start))  # Сменить валюту
    dp.add_handler(CommandHandler("select", start))  # Выбрать другую валюту
    dp.add_handler(CommandHandler("choose", start))  # Выбрать валюту
    dp.add_handler(CommandHandler("switch", start))  # Сменить валюту
    dp.add_handler(CommandHandler("reselect", start))  # Пересоздать меню выбора
    dp.add_handler(CommandHandler("refresh", start))  # Обновить меню
    dp.add_handler(CommandHandler("reset", start))  # Начать заново
    dp.add_handler(CommandHandler("go", start))  # Перезапуск бота
    dp.add_handler(CommandHandler("again", start))  # Повторить
    dp.add_handler(CommandHandler("more", start))  # Дополнительно
    dp.add_handler(CommandHandler("list", start))  # Список валют
    dp.add_handler(CommandHandler("options", start))  # Опции
    dp.add_handler(CommandHandler("info", start))  # Информация
    dp.add_handler(CommandHandler("about", start))  # О боте
    dp.add_handler(CommandHandler("details", start))  # Подробности
    dp.add_handler(CommandHandler("contact", start))  # Контакты
    dp.add_handler(CommandHandler("support", start))  # Поддержка
    dp.add_handler(CommandHandler("faq", start))  # Частые вопросы
    dp.add_handler(CommandHandler("feedback", start))  # Отзывы
    dp.add_handler(CommandHandler("report", start))  # Сообщить о проблеме
    dp.add_handler(CommandHandler("issue", start))  # Проблема
    dp.add_handler(CommandHandler("bug", start))  # Баг
    dp.add_handler(CommandHandler("error", start))  # Ошибка
    dp.add_handler(CommandHandler("fix", start))  # Исправить
    dp.add_handler(CommandHandler("solution", start))  # Решение
    dp.add_handler(CommandHandler("update", start))  # Обновить
    dp.add_handler(CommandHandler("news", start))  # Новости
    dp.add_handler(CommandHandler("latest", start))  # Последние обновления
    dp.add_handler(CommandHandler("version", start))  # Версия
    dp.add_handler(CommandHandler("release", start))  # Выпуск

    updater.start_polling()
    updater.idle()

if _name_ == "_main_":
    main()
