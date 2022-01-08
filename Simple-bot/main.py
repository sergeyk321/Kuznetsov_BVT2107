import telebot
from telebot import types

bot = telebot.TeleBot("Enter your token")

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/start", "/help", "/music","/days", "Хочу", "Кто тебя создал?", "Как дела?")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)
@bot.message_handler(commands=['days'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","/back")
    bot.send_message(message.chat.id, 'Выберите день', reply_markup=keyboard)
@bot.message_handler(commands=['back'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/start", "/help", "/music","/days", "Хочу", "Кто тебя создал?", "Как дела?")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Доступные команды: /start, /help, Кто тебя создал, Как дела?, Хочу')
@bot.message_handler(commands=['music'])
def start(message):
    bot.send_message(message.chat.id, 'Mayot, Платина, OG Buda, Дора')
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')
    if message.text.lower() == "кто тебя создал?":
        bot.send_message(message.chat.id, 'Сергей Кузнецов, студент группы БВТ2107')
    if message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, 'Отлично!')


bot.polling(none_stop=True, interval=0)

