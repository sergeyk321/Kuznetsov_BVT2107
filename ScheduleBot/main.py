from datetime import datetime, date, time
import telebot 
from telebot import types
import psycopg2

bot = telebot.TeleBot("Enter your token")

conn = psycopg2.connect(database="telegramschedule",
                        user="postgres",
                        password="1",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

start = date(2021, 9, 1)
d = datetime.now()
week = d.isocalendar()[1] - start.isocalendar()[1] + 1

if week/2 == 1:
    num_week = True
    text_week = "ODD"
    ru_text_week = "чётной"
    nottext_week = "EVEN"
else:
    num_week = False
    text_week = "EVEN"
    ru_text_week = "нечётной"
    nottext_week = "ODD"

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/start", "/help","/days","/mtuci","/week","Кто тебя создал?")
    keyboard.row("Расписание на эту неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)
@bot.message_handler(commands=['days'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота","/back")
    bot.send_message(message.chat.id, 'Выберите день', reply_markup=keyboard)
@bot.message_handler(commands=['back'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/start", "/help","/days","/mtuci","/week","Кто тебя создал?")
    keyboard.row("Расписание на эту неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)

@bot.message_handler(commands=['mtuci'])
def start(message):
    bot.send_message(message.chat.id, 'Сайт МТУСИ: https://mtuci.ru/')

@bot.message_handler(commands = ['week'])
def week(message):
    if num_week == True:
        bot.send_message(message.chat.id, 'верхняя')
    else:
        bot.send_message(message.chat.id, 'нижняя')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Данный бот показывает расписание группы БВТ2107\n\
Чтобы узнать расписание, введите команду /days и выберите нужный день\n\
Чтобы узнать, какая сейчас неделя, введите команду /week\n\
Сайт МТУСИ: /mtuci')

@bot.message_handler(content_types =['text'])
def answer(message):
    if message.text.lower() == "кто тебя создал?":
        bot.send_message(message.chat.id, 'Сергей Кузнецов, студент группы БВТ2107')
    if message.text.lower() == "расписание на эту неделю":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE week = 'ALWAYS' or week = '{text_week}'\
                        ORDER BY timetable.id, timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на эту неделю:")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    if message.text.lower() == "расписание на следующую неделю":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE week = 'ALWAYS' or week = '{text_week}'\
                        ORDER BY timetable.id, timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на следующую неделю:")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    if message.text.lower() == "понедельник":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE day = 'Понедельник' and (week = 'ALWAYS' or week = '{text_week}')\
                        ORDER BY timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на понедельник (по {ru_text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    elif message.text.lower() == "вторник":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE day = 'Вторник' and (week = 'ALWAYS' or week = '{text_week}')\
                        ORDER BY timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на вторник (по {ru_text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    elif message.text.lower() == "среда":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE day = 'Среда' and (week = 'ALWAYS' or week = '{text_week}')\
                        ORDER BY timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на среду (по {ru_text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    elif message.text.lower() == "четверг":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE day = 'Четверг' and (week = 'ALWAYS' or week = '{text_week}')\
                        ORDER BY timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на четверг (по {ru_text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    elif message.text.lower() == "пятница":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE day = 'Пятница' and (week = 'ALWAYS' or week = '{text_week}')\
                        ORDER BY timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на пятницу (по {ru_text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    elif message.text.lower() == "суббота":
        cursor.execute(f"SELECT subject.subject_name, timetable.room_numb, timetable.start_time, teacher.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject_id\
                        INNER JOIN teacher ON subject.id = teacher.fk_subject\
                        WHERE day = 'Суббота' and (week = 'ALWAYS' or week = '{text_week}')\
                        ORDER BY timetable.start_time")
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на субботу (по {ru_text_week} неделе):")
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")

    
        

bot.polling(none_stop=True, interval=0)








