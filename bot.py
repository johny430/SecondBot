import telebot
from telebot import types
import json
import requests
import sqlite3
import threading
from random import randint
import time
from datetime import datetime
import hashlib
import random

bot = telebot.TeleBot('1194122886:AAEh8HEUsCHnrCNpjlsX15REDyp4eLsvAbk')
api_token = ''
group_id = -466351524
payment_group_id = -482890684
task_group_id = -498501871
coef = 0.036
qiwi_api_access_token = '53afd9e2ae19f16f12df0d7e3f97586c'
phone_number = '+380505679034'
nickname = ''

jsan = {
    'ВКонтакте': {
        '❤️ Лайки': 2,
        '👥 Участники': 4,
        '👤 Друзья': 4,
        '🔁 Репосты': 4,
        '📢 Голоса в опросе': 2,
    },
    'Ютуб': {
        '❤️ Лайки': 6,
        '👥 Подписчики': 6,
        '💔 Дизлайки': 5,
        '💕 Лайки на комментарий': 2,
    },
    'Инстаграмм': {
        '❤️ Лайки': 3,
        '👥 Подписчики': 4,
        '💕 Лайки на комментарий': 2,
    },
    'Телеграм': {
        '👥 Подписчики': 4,
    },
    'Одноклассники': {
        '👍 Классы': 3,
        '👤 Друзья': 3,
        '👥 Подписчики': 3,
    },
    'Твиттер': {
        '🔁 Ретвиты': 5,
        '👥 Фолловеры': 5,
        '❤️ Лайки': 5,
},
}

forapi = {
    'ВКонтакте': {
        '❤️ Лайки': "likes",
        '👥 Участники': 'groups',
        '👤 Друзья': 'friends',
        '🔁 Репосты': "reposts",
        '📢 Голоса в опросе': "polls",
    },
    'Ютуб': {
        '❤️ Лайки': "likes",
        '👥 Подписчики': 6,
        '💔 Дизлайки': 'dislikes',
        '💕 Лайки на комментарий': "comments_likes",
    },
    'Инстаграмм': {
        '❤️ Лайки': "likes",
        '👥 Подписчики': 'subscribers',
        '💕 Лайки на комментарий': "comments_likes",
    },
    'Телеграм': {
        '👥 Подписчики': 'subscribers',
    },
    'Одноклассники': {
        '👍 Классы': "likes",
        '👤 Друзья': "friends",
        '👥 Подписчики': 'groups',
    },
    'Твиттер': {
        '🔁 Ретвиты': "retweets",
        '👥 Фолловеры': "followers",
        '❤️ Лайки': "favorites",
},
}

speeds = {
    'ВКонтакте':{
        '❤️ Лайки':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
            },
        '👤 Друзья':{
            'Обычный' : 4,
            'Быстрый' : 6,
        },
        '🔁 Репосты':{
            'Обычный': 4,
            'Быстрый' : 6,
            },
        '👥 Участники':{
            'Обычный': 4,
            'Быстрый' : 7,
        },
        '📢 Голоса в опросе':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
        },
    },
    'Инстаграмм':{
        '❤️ Лайки':{
            'Обычный' : 3,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
        },
        '👥 Подписчики':{
            'Обычный' : 4,
            'Быстрый' : 7,
        },
        '💕 Лайки на комментарий':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
        },
    },
    'Ютуб':{
        '❤️ Лайки':{
            'Обычный' : 6,
            'Быстрый' : 9,
    },
        '💔 Дизлайки':{
            'Обычный' : 5,
            'Быстрый' : 10,
    },
        '👥 Подписчики':{
            'Обычный' : 6,
            'Быстрый' : 9,
    },
        '💕 Лайки на комментарий':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
},
    },
    'Телеграм':{
        '👥 Подписчики':{
            'Обычный' : 4,
            'Быстрый' : 7,
        },
},
    'Одноклассники':{
        '👍 Классы':{
            'Обычный' : 3,
            'Быстрый' : 6,
        },
        '👤 Друзья':{
            'Обычный' : 3,
            'Быстрый' : 6,
        },
        '👥 Подписчики':{
            'Обычный' : 3,
            'Быстрый' : 6,
        },
},
    'Твиттер':{
        '🔁 Ретвиты':{
            'Обычный' : 5,
            'Быстрый' : 10,
        },
        '👥 Фолловеры':{
            'Обычный' : 5,
            'Быстрый': 10,
        },
        '❤️ Лайки':{
            'Обычный' : 5,
            'Быстрый' : 10,
        },
},
}

mytasks_btn = types.KeyboardButton("📋 Мои задания")
sootv = {"ВКонтакте": "vk", "Телеграм": "telegram", "Инстаграмм": "instagram", "Твиттер": "twitter","Одноклассники": "ok", "Ютуб": "youtube"}

menubuttion = types.KeyboardButton("Меню")

markupkupon = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn0 = types.KeyboardButton("↩️ Назад")
item10 = types.KeyboardButton("Ввести купон")
markupkupon.add(btn0, item10)

markupopl2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn0 = types.KeyboardButton("↩️ Назад")
pppl = types.KeyboardButton("💳 Пополнить")
markupopl2.add(btn0,pppl)
markupnone = types.ReplyKeyboardMarkup(resize_keyboard=True)

kuda = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("ВКонтакте")
btn2 = types.KeyboardButton("Телеграм")
btn3 = types.KeyboardButton("Инстаграмм")
btn4 = types.KeyboardButton("Твиттер")
btn5 = types.KeyboardButton("Одноклассники")
btn6 = types.KeyboardButton("Ютуб")
kuda.add(btn1, btn2, btn3,btn4,btn5,btn6,btn0)

markupopl3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
item111 = types.KeyboardButton("✅ Оплатил(a)")
markupopl3.add(item111,btn0)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn1 = types.KeyboardButton("🚀 Накрутить")
btn2 = types.KeyboardButton("💰 Баланс")
btn3 = types.KeyboardButton("✉️ Репорт")
apravilabtn3 = types.KeyboardButton("📜 Правила")
markup.add(btn1, btn2, btn3, mytasks_btn, apravilabtn3)

btn_2 = types.KeyboardButton("💔 Дизлайки")
btn_1 = types.KeyboardButton("👥 Участники")
btn1 = types.KeyboardButton("❤️ Лайки")
btn2 = types.KeyboardButton("👤 Друзья")
btn3 = types.KeyboardButton("🔁 Репосты")
btn4 = types.KeyboardButton("Комментарии")
btn5 = types.KeyboardButton("📢 Голоса в опросе")
btn6 = types.KeyboardButton("👥 Подписчики")
btn7 = types.KeyboardButton("💕 Лайки на комментарий")
btn8 = types.KeyboardButton("💔 Дизлайки")
btn9 = types.KeyboardButton("👤 Друзья")
btn10 = types.KeyboardButton("👍 Классы")
btn11 = types.KeyboardButton("🔁 Ретвиты")
btn12 = types.KeyboardButton("👥 Фолловеры")
vk = types.ReplyKeyboardMarkup(resize_keyboard=True)
tg = types.ReplyKeyboardMarkup(resize_keyboard=True)
inst = types.ReplyKeyboardMarkup(resize_keyboard=True)
twt = types.ReplyKeyboardMarkup(resize_keyboard=True)
odnkl = types.ReplyKeyboardMarkup(resize_keyboard=True)
youtube = types.ReplyKeyboardMarkup(resize_keyboard=True)
vk.add(btn1,btn2,btn3,btn5,btn_1,btn0)
inst.add(btn1,btn6,btn7,btn0)
youtube.add(btn1,btn6,btn7,btn_2,btn0)
tg.add(btn6,btn0)
odnkl.add(btn9,btn10,btn6,btn0)
twt.add(btn12,btn11,btn1,btn0)

markupnazad = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markupnazad.add(btn0)

markupopl = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btnopl = types.KeyboardButton("Оплатить")
markupopl.add(btn0,btnopl)

markupchtos = types.ReplyKeyboardMarkup(row_width = 1)
anypay = types.KeyboardButton('🔗 AnyPay (остальные платежные системы)')
qiwis = types.KeyboardButton('🥝 Qiwi')
markupchtos.add(anypay,qiwis,btn0)

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            dannie = [int(message.from_user.id),float(0),int(0)]
            c.execute("INSERT OR IGNORE INTO Users VALUES (?,?,?)", dannie)
            conn.commit()
            bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 Накрутить")
def krt(message):
    if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = ((int(message.chat.id)),)
            c.execute('SELECT * FROM zadania WHERE id = ?', t)
            e = c.fetchall()
            if int(len(e)) >= 10:
                bot.send_message(message.chat.id, '⛔️ У вас слишком много активных заданий!', reply_markup=markup)
            else:
                msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
                bot.register_next_step_handler(msg, chto)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

def chto(message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = (int(message.chat.id),)
    c.execute("""DELETE from tzadania where id = ?""", t)
    conn.commit()
    if message.text == "ВКонтакте":
        b = str(message.text)
        t = int(message.chat.id)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        data2 = [t, b, 0, 0, 0, 0, 0,0]
        c.execute("INSERT INTO tzadania VALUES (?,?,?,?,?,?,?,?)", data2)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=vk)
        bot.register_next_step_handler(msg, next)
    elif message.text == 'Телеграм':
        b = str(message.text)
        t = int(message.chat.id)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        data2 = [t, b, 0, 0, 0, 0, 0,0]
        c.execute("INSERT INTO tzadania VALUES (?,?,?,?,?,?,?,?)", data2)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=tg)
        bot.register_next_step_handler(msg, teg)
    elif message.text == 'Инстаграмм':
        b = str(message.text)
        t = int(message.chat.id)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        data2 = [t, b, 0, 0, 0, 0, 0, 0]
        c.execute("INSERT INTO tzadania VALUES (?,?,?,?,?,?,?,?)", data2)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=inst)
        bot.register_next_step_handler(msg, insta)
    elif message.text == 'Твиттер':
        b = str(message.text)
        t = int(message.chat.id)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        data2 = [t, b, 0, 0, 0, 0, 0, 0]
        c.execute("INSERT INTO tzadania VALUES (?,?,?,?,?,?,?,?)", data2)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=twt)
        bot.register_next_step_handler(msg, twter)
    elif message.text == 'Одноклассники':
        b = str(message.text)
        t = int(message.chat.id)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        data2 = [t, b, 0, 0, 0, 0, 0, 0]
        c.execute("INSERT INTO tzadania VALUES (?,?,?,?,?,?,?,?)", data2)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=odnkl)
        bot.register_next_step_handler(msg, odnoklas)
    elif message.text == 'Ютуб':
        b = str(message.text)
        t = int(message.chat.id)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        data2 = [t, b, 0, 0, 0, 0, 0, 0]
        c.execute("INSERT INTO tzadania VALUES (?,?,?,?,?,?,?,?)", data2)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=youtube)
        bot.register_next_step_handler(msg, youtab)
    elif message.text == '↩️ Назад':
        t = (int(message.chat.id),)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("""DELETE from tzadania where id = ?""", t)
        conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)

def next(message):
    spisok1 = ["❤️ Лайки", "👤 Друзья", "🔁 Репосты","👥 Участники"]
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    elif str(message.text) == "📢 Голоса в опросе":
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, nextvk)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=vk)
        bot.register_next_step_handler(msg, next)

def nextvk(message):
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=vk)
        bot.register_next_step_handler(msg, next)
    elif message.text == None:
        msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, nextvk)
    elif message.text.isdigit():
        if int(message.text) > 0:
            o = int(message.text)
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            sql = """
            UPDATE tzadania
            SET polls = ? 
            WHERE id = ?
            """
            data = (o, int(message.from_user.id))
            c.execute(sql, data)
            conn.commit()
            msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:", reply_markup=markupnazad)
            bot.register_next_step_handler(msg, next2)
        else:
            msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:",reply_markup=markupnazad)
            bot.register_next_step_handler(msg, nextvk)
    else:
        msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, nextvk)

def teg(message):
    spisok1 = ["👥 Подписчики"]
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=tg)
        bot.register_next_step_handler(msg, teg)

def insta(message):
    spisok1 = ["❤️ Лайки","👥 Подписчики","💕 Лайки на комментарий"]
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=inst)
        bot.register_next_step_handler(msg, insta)

def twter(message):
    spisok1 = ["❤️ Лайки","👥 Фолловеры","🔁 Ретвиты"]
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=twt)
        bot.register_next_step_handler(msg, twter)

def odnoklas(message):
    spisok1 = ["👥 Подписчики","👍 Классы","👤 Друзья"]
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=odnkl)
        bot.register_next_step_handler(msg, odnoklas)

def youtab(message):
    spisok1 = ["👥 Подписчики","❤️ Лайки","💕 Лайки на комментарий","💔 Дизлайки"]
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        e = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET chto = ? 
        WHERE id = ?
        """
        data = (e, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, 'Введите ссылку куда нужно произвести накрутку:',reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=youtube)
        bot.register_next_step_handler(msg, youtab)

def next2(message):
    if message.text == '↩️ Назад':
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ((int(message.chat.id)),)
        c.execute('SELECT * FROM tzadania WHERE id = ?', t)
        e = c.fetchone()
        b = e[1]
        if b == "ВКонтакте":
            msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=vk)
            bot.register_next_step_handler(msg, next)
        elif b == 'Телеграм':
            msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=tg)
            bot.register_next_step_handler(msg, teg)
        elif b == 'Инстаграмм':
            msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=inst)
            bot.register_next_step_handler(msg, insta)
        elif b == 'Твиттер':
            msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=twt)
            bot.register_next_step_handler(msg, twter)
        elif b == 'Одноклассники':
            msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=odnkl)
            bot.register_next_step_handler(msg, odnoklas)
        elif b == 'Ютуб':
            msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=youtube)
            bot.register_next_step_handler(msg, youtab)
        #bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    else:
        g = str(message.text)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        sql = """
        UPDATE tzadania
        SET url = ? 
        WHERE id = ?
        """
        data = (g, int(message.from_user.id))
        c.execute(sql, data)
        conn.commit()
        msg = bot.send_message(message.chat.id, "Выберите количество:",reply_markup=markupnone)
        bot.register_next_step_handler(msg, next3)

def next3(message):
    g = str(message.text)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = ((int(message.chat.id)),)
    c.execute('SELECT * FROM tzadania WHERE id = ?', t)
    a = c.fetchone()
    x = str(a[1])
    e = str(a[2])
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Введите ссылку куда нужно произвести накрутку:',reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    elif message.text == None:
        msg = bot.send_message(message.chat.id, "Выберите количество:", reply_markup=markupnone)
        bot.register_next_step_handler(msg, next3)
    elif message.text.isdigit():
        if int(message.text) < 5:
            msg = bot.send_message(message.chat.id, "Минимально 5\n\nУкажите верное количество:", reply_markup=markupnone)
            bot.register_next_step_handler(msg, next3)
        elif int(message.text) >= 2000:
            q = int(message.text)
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            sql = """
            UPDATE tzadania
            SET colvo = ? 
            WHERE id = ?
            """
            data = (q, int(message.from_user.id))
            c.execute(sql, data)
            conn.commit()
            markupSPEED = types.ReplyKeyboardMarkup(row_width=1)
            aloxa = list(speeds[x][e])
            for i in range(len(aloxa)):
                atatat = types.KeyboardButton(str(aloxa[i]))
                markupSPEED.add(atatat)
            markupSPEED.add(btn0)
            msg = bot.send_message(message.chat.id, "Хорошо, выберите режим скорости:",reply_markup=markupSPEED)
            bot.register_next_step_handler(msg, rejim)
        else:
            try:
                q = int(message.text)
                f = int(jsan[x][e])
                l = f * q * coef
                l = round(l, 2)
                kaaaaa = 'Обычный'
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                sql = """
                UPDATE tzadania
                SET sum = ? 
                WHERE id = ?
                """
                data = (l, int(message.from_user.id))
                c.execute(sql, data)
                sql = """
                UPDATE tzadania
                SET colvo = ? 
                WHERE id = ?
                """
                data = (q, int(message.from_user.id))
                c.execute(sql, data)
                sql = """
                UPDATE tzadania
                SET speed = ? 
                WHERE id = ?
                """
                data = (kaaaaa, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - "+str(l)+"₽",reply_markup=markupopl)
                bot.register_next_step_handler(msg, next4)
            except:
                bot.send_message(message.chat.id, "⛔️ Что-то пошло не так! :(", reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, "Введите количество:", reply_markup=markupnone)
        bot.register_next_step_handler(msg, next3)

def rejim(message):
    g = str(message.text)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    t = ((int(message.chat.id)),)
    c.execute('SELECT * FROM tzadania WHERE id = ?', t)
    a = c.fetchone()
    x = str(a[1])
    e = str(a[2])
    q = int(a[4])
    aloxa = list(speeds[x][e])
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, "Введите количество:", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next3)
    elif str(message.text) in aloxa:
        try:
            f = int(jsan[x][e])
            kaaaaa = str(message.text)
            if message.text == 'Обычный':
                kaaaaa = str(message.text)
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                sql = """
                UPDATE tzadania
                SET speed = ? 
                WHERE id = ?
                """
                data = (kaaaaa, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                l = f * q * coef
                l = round(l, 2)
                sql = """
                UPDATE tzadania
                SET sum = ? 
                WHERE id = ?
                """
                data = (l, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - " + str(l) + "₽",reply_markup=markupopl)
                bot.register_next_step_handler(msg, next4)
            elif message.text == 'Быстрый':
                kaaaaa = str(message.text)
                c = conn.cursor()
                sql = """
                UPDATE tzadania
                SET speed = ? 
                WHERE id = ?
                """
                data = (kaaaaa, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                l = f * q * coef * 2
                l = round(l, 2)
                sql = """
                UPDATE tzadania
                SET sum = ? 
                WHERE id = ?
                """
                data = (l, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - " + str(l) + "₽",reply_markup=markupopl)
                bot.register_next_step_handler(msg, next4)
            elif message.text == 'Очень быстрый':
                kaaaaa = str(message.text)
                c = conn.cursor()
                sql = """
                UPDATE tzadania
                SET speed = ? 
                WHERE id = ?
                """
                data = (kaaaaa, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                l = f * q * coef * 3
                l = round(l, 2)
                sql = """
                UPDATE tzadania
                SET sum = ? 
                WHERE id = ?
                """
                data = (l, int(message.from_user.id))
                c.execute(sql, data)
                conn.commit()
                msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - " + str(l) + "₽",reply_markup=markupopl)
                bot.register_next_step_handler(msg, next4)
        except:
            bot.send_message(message.chat.id, "⛔️ Что-то пошло не так! :(", reply_markup=markup)
    else:
        markupSPEED = types.ReplyKeyboardMarkup(row_width=1)
        aloxa = list(speeds[x][e])
        for i in range(len(aloxa)):
            atatat = types.KeyboardButton(str(aloxa[i]))
            markupSPEED.add(atatat)
        markupSPEED.add(btn0)
        msg = bot.send_message(message.chat.id, "Хорошо, выберите режим скорости:", reply_markup=markupSPEED)
        bot.register_next_step_handler(msg, rejim)

def next4(message):
    try:
        if message.text == '↩️ Назад':
            msg = bot.send_message(message.chat.id, "Введите количество:", reply_markup=markupnazad)
            bot.register_next_step_handler(msg, next3)
        elif message.text == 'Оплатить':
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            conn = sqlite3.connect('example.db')
            t = ((int(message.chat.id)),)
            c.execute('SELECT * FROM tzadania WHERE id = ?', t)
            eptoooo = c.fetchone()
            if str(eptoooo[2]) == '📢 Голоса в опросе':
                data = [int(message.chat.id),str(eptoooo[1]),str(eptoooo[2]),str(eptoooo[3]),str(eptoooo[4]),str(eptoooo[6]),str(eptoooo[7])]
            else:
                data = [int(message.chat.id),str(eptoooo[1]), str(eptoooo[2]), str(eptoooo[3]), str(eptoooo[4]),str(eptoooo[7])]
            c.execute('SELECT * FROM users WHERE id=?', t)
            a = c.fetchone()
            l = eptoooo[5]
            q = int(eptoooo[4])
            if a[1] < l:
                bot.send_message(message.chat.id, 'Для накрутки не достаточно средств\n\nПополнить баланс можно в главном меню',reply_markup=markup)
            else:
                if len(data) == 6:
                    a = sootv[data[1]]
                    p = forapi[data[1]][data[2]]
                    c = data[3]
                    d = data[4]
                    f = data[5]
                    pl = speeds[data[1]][data[2]][data[5]]
                    data2 = [int(message.from_user.id),data[1],data[2],c,d,l]
                    params = {'api_token': api_token, 'network': a,'section': p,'link': c,'count': q, 'amount': pl}
                    rng1 = random.randint(1, 3)
                    rng2 = random.uniform(0.1, 1)
                    zad_time = rng2 * rng1
                    time.sleep(zad_time)
                    r = requests.get('https://vkmix.com/api/2/createTask', params=params)
                    ar = r.text
                    if ar.startswith('{"error":'):
                        bot.send_message(message.chat.id, '⛔️ Мне не удалось создать задание',reply_markup=markup)
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        t = (int(message.chat.id),)
                        c.execute("""DELETE from tzadania where id = ?""", t)
                        conn.commit()
                    else:
                        task_id = r.json()["response"]["id"]
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        t = int(message.chat.id)
                        t = (t,)
                        c.execute('SELECT * FROM users WHERE id=?', t)
                        a = c.fetchone()
                        pox = float(a[1])
                        b = pox - float(l)
                        b = round(b, 2)
                        sql = """
                        UPDATE users
                        SET balance = ? 
                        WHERE id = ?
                        """
                        data = (b, int(message.from_user.id))
                        c.execute(sql, data)
                        conn.commit()
                        c.execute('SELECT * FROM nomezad')
                        apchu = c.fetchone()
                        now = datetime.now()
                        current_time = now.strftime("%d.%m.%y в %H:%M")
                        apchu = int(apchu[0])
                        apchu = apchu + 1
                        data2.append(apchu)
                        data2.append(task_id)
                        data2.append(current_time)
                        bot.send_message(message.chat.id, "✅ Задание успешно создано, его персональный номер - #"+str(data2[6]),reply_markup=markup)
                        c.execute("INSERT INTO zadania VALUES (?,?,?,?,?,?,?,?,?)",data2)
                        now = datetime.now()
                        current_time = now.strftime("%d.%m.%y в %H:%M")
                        msg = bot.send_message(task_group_id, '📋 Создано новое задание #' + str(apchu) + '\n\nКто создал: ' + str(message.from_user.id) + '\nTelegram ник: @' + str(message.from_user.username) + '\nКакая соц.сеть выбрана: ' + str(eptoooo[1]) + '\nЧто выбрано для накрутки: ' + str(eptoooo[2]) + '\nКуда выполняется накрутка: '+str(eptoooo[3])+'\nКоличество: ' + str(eptoooo[4]) + '\nСумма: ' + str(l) + "₽" + '\nВремя: ' + str(current_time)+'\n\nСтатус: Не выполнен')# (0/'+str(data2[4])+')')
                        sql = """
                        UPDATE nomezad
                        SET num = ? 
                        WHERE num = ?
                        """
                        data = (apchu, int(apchu - 1))
                        c.execute(sql, data)
                        conn.commit()
                        data13 = [int(msg.message_id),str(msg.text),int(task_id)]
                        c.execute("INSERT INTO tasks_status VALUES (?,?,?)", data13)
                        conn.commit()
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        t = (int(message.chat.id),)
                        c.execute("""DELETE from tzadania where id = ?""", t)
                        conn.commit()
                else:
                    a = sootv[data[1]]
                    p = forapi[data[1]][data[2]]
                    c = data[3]
                    d = data[4]
                    f = data[5]
                    pl = speeds[data[1]][data[2]][data[6]]
                    data2 = [int(message.from_user.id),data[1],data[2],c,d,f]
                    o = data[5]
                    params = {'api_token': api_token, 'network': a,'section': p,'link': c,'count': q, 'amount': pl,'poll':o}
                    rng1 = random.randint(1, 3)
                    rng2 = random.uniform(0.1, 1)
                    zad_time = rng2 * rng1
                    time.sleep(zad_time)
                    r = requests.get('https://vkmix.com/api/2/createTask', params=params)
                    ar = r.text
                    if ar.startswith('{"error":'):
                        bot.send_message(message.chat.id, '⛔️ Мне не удалось создать задание', reply_markup=markup)
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        t = (int(message.chat.id),)
                        c.execute("""DELETE from tzadania where id = ?""", t)
                        conn.commit()
                    else:
                        task_id = r.json()["response"]["id"]
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        t = int(message.chat.id)
                        t = (t,)
                        c.execute('SELECT * FROM users WHERE id=?', t)
                        a = c.fetchone()
                        pox = float(a[1])
                        b = pox - float(l)
                        b = round(b, 2)
                        sql = """
                        UPDATE users
                        SET balance = ? 
                        WHERE id = ?
                        """
                        data = (b, int(message.from_user.id))
                        c.execute(sql, data)
                        conn.commit()
                        c.execute('SELECT * FROM nomezad')
                        apchu = c.fetchone()
                        now = datetime.now()
                        current_time = now.strftime("%d.%m.%y в %H:%M")
                        apchu = int(apchu[0])
                        apchu = apchu + 1
                        data2.append(apchu)
                        data2.append(task_id)
                        data2.append(current_time)
                        bot.send_message(message.chat.id,"✅ Задание успешно создано, его персональный номер - #" + str(data2[6]),reply_markup=markup)
                        c.execute("INSERT INTO zadania VALUES (?,?,?,?,?,?,?,?,?)", data2)
                        now = datetime.now()
                        current_time = now.strftime("%d.%m.%y в %H:%M")
                        msg = bot.send_message(task_group_id,'📋 Создано новое задание #' + str(apchu) + '\n\nКто создал: ' + str(message.from_user.id) + '\nTelegram ник: @' + str(message.from_user.username) + '\nКакая соц.сеть выбрана: ' + str(eptoooo[1]) + '\nЧто выбрано для накрутки: ' + str(eptoooo[2]) + '\nКуда выполняется накрутка: ' + str(eptoooo[3]) + '\nКоличество: ' + str(eptoooo[4]) + '\nСумма: ' + str(l) + "₽" + '\nВремя: ' + str(current_time) + '\n\nСтатус: Не выполнен')  # (0/'+str(data2[4])+')')
                        sql = """
                        UPDATE nomezad
                        SET num = ? 
                        WHERE num = ?
                        """
                        data = (apchu, int(apchu - 1))
                        c.execute(sql, data)
                        conn.commit()
                        data13 = [int(msg.message_id), str(msg.text), int(task_id)]
                        c.execute("INSERT INTO tasks_status VALUES (?,?,?)", data13)
                        conn.commit()
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        t = (int(message.chat.id),)
                        c.execute("""DELETE from tzadania where id = ?""", t)
                        conn.commit()
        else:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            conn = sqlite3.connect('example.db')
            t = ((int(message.chat.id)),)
            c.execute('SELECT * FROM tzadania WHERE id = ?', t)
            eptoooo = c.fetchone()
            l = eptoooo[5]
            msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - "+str(l)+"₽",reply_markup=markupopl)
            bot.register_next_step_handler(msg, next4)
    except:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (int(message.chat.id),)
            c.execute("""DELETE from tzadania where id = ?""", t)
            conn.commit()
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 Баланс")
def balance(message):
    global  markupchto
    markupchto = types.ReplyKeyboardMarkup(row_width = 1)
    anypay = types.KeyboardButton('🔗 AnyPay (остальные платежные системы)')
    qiwis = types.KeyboardButton('🥝 Qiwi')
    markupchto.add(anypay,qiwis,btn0)
    if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        global  a
        a = int(message.from_user.id)
        t = (a,)
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE id=?', t)
            a = c.fetchone()
            msg = bot.send_message(message.chat.id, "Ваш баланс: "+str(a[1])+" ₽",reply_markup=markupopl2)
            bot.register_next_step_handler(msg, balance2)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

def balance2(message):
    if message.text == '↩️ Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    elif message.text == "💳 Пополнить":
        msg = bot.send_message(message.chat.id, "Выберите платежную систему:", reply_markup=markupchto)
        bot.register_next_step_handler(msg, chtos)
    else:
        msg = bot.send_message(message.chat.id, "Ваш баланс: " + str(a[1]) + "₽", reply_markup=markupopl2)
        bot.register_next_step_handler(msg, balance2)

def chtos(message):
    if message.text == '↩️ Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    elif message.text  == '🔗 AnyPay (остальные платежные системы)':
        msg2 = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg2, anypays)
    elif message.text  == '🥝 Qiwi':
        msg4 = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg4, balance3)
    else:
        msg = bot.send_message(message.chat.id, "Выберите платежную систему:", reply_markup=markupchto)
        bot.register_next_step_handler(msg, chtos)

def anypays(message):
    global yes
    if message.text == '↩️ Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text == None:
        msg = bot.send_message(message.chat.id, "Выберите платежную систему:", reply_markup=markupchto)
        bot.register_next_step_handler(msg, chtos)
    elif message.text.isdigit() and int(message.text) > 4:
        try:
            yes = str(message.text)
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM nomeranypay')
            a = c.fetchone()
            a = int(a[0])
            a = a + 1
            ax = str(a)
            project_id = '5813'
            amount = yes
            currency = 'RUB'
            pay_id = ax
            secret_key = 'bVWgGA6EoEoHllo6Tql8yCj'
            arr_sign = bytes(f'{currency}:{amount}:{secret_key}:{project_id}:{pay_id}', encoding='utf-8')
            result = hashlib.md5(arr_sign)
            a = result.hexdigest()
            a = str(a)
            params = {'merchant_id': project_id, 'amount': amount,'desc':'Выберите платежную систему','currency': currency, 'pay_id': pay_id, 'sign': a}
            r = requests.get('https://anypay.io/merchant', params=params)
            ek = str(r.url)
            data = [int(message.from_user.id), ax, yes]
            c.execute("INSERT INTO payments VALUES (?,?,?)", data)
            conn.commit()
            sql = """
            UPDATE nomeranypay
            SET num = ? 
            WHERE num = ?
            """
            ax = int(ax)
            data = (int(ax), int(ax - 1))
            c.execute(sql, data)
            conn.commit()
            msg = bot.send_message(message.chat.id,'Сумма: ' + str(yes) + '\nПополнить баланс можно по ссылке ниже:\n' + str(ek), reply_markup=markupopl3, parse_mode='html')
            bot.register_next_step_handler(msg, balance5)
            conn.commit()
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, anypays)

def balance5(message):
    if message.text == '↩️ Назад':
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            id = str(message.from_user.id)
            t = (id,)
            c.execute("""DELETE from payments where id = ?""", t)
            conn.commit()
            bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)
    elif message.text == '✅ Оплатил(a)':
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            id = str(message.from_user.id)
            t = (id,)
            c.execute('SELECT * FROM payments WHERE id=?', t)
            eka = c.fetchone()
            pay_id = str(eka[1])
            m = hashlib.sha256()
            m.update(b"payments5E24FF1B50BE374C76DC5813fkPEItrHxTvT9LzbXbCIj4BheRSuKLumYGcdE2u")
            a = m.hexdigest()
            params = {'project_id': '5813', 'sign': a,'pay_id':pay_id}
            r = requests.get('https://anypay.io/api/payments/5E24FF1B50BE374C76DC', params=params)
            a = r.json()
            if a['result']['payments'] == None:
                msg = bot.send_message(message.chat.id,'Оплата не найдена!',reply_markup=markupopl3, parse_mode='html')
                bot.register_next_step_handler(msg, balance5)
            else:
                e = list(a['result']['payments'])
                if a['result']['payments'][e[0]]["pay_id"] == int(pay_id):
                    if a['result']['payments'][e[0]]["status"] == "paid":
                        rng1 = random.randint(1, 1)
                        rng2 = random.uniform(0.1, 1)
                        zad_time = rng2 * rng1
                        time.sleep(zad_time)
                        a = int(yes)
                        t = (int(message.chat.id),)
                        c.execute("""DELETE from payments where id = ?""", t)
                        t = (int(message.chat.id),)
                        c.execute('SELECT * FROM users WHERE id=?', t)
                        g = c.fetchone()
                        b = float(g[1]) + float(a)
                        b = round(b, 2)
                        sql = """
                        UPDATE users
                        SET balance = ? 
                        WHERE id = ?
                        """
                        t = int(message.chat.id)
                        data = (b, t)
                        c.execute(sql, data)
                        conn.commit()
                        bot.send_message(message.chat.id, 'Оплата произведена успешно. Ваш новый баланс: ' + str(b) + '₽',reply_markup=markup)
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        c.execute('SELECT * FROM nomeraoplati')
                        opa = c.fetchone()
                        opa = opa[0]
                        opa = int(opa)
                        opa = opa + 1
                        now = datetime.now()
                        current_time = now.strftime("%d.%m.%y в %H:%M")
                        bot.send_message(payment_group_id, "💰 Новая оплата #" + str(opa) + "\n\nСумма: " + str(a) + "₽" + "\nОплачено: AnyPay\nКто оплатил: " + str(message.from_user.id) + "\nTelegram никнейм: @" + str(message.from_user.username) + "\nВремя: " + str(current_time))
                        sql = """
                        UPDATE nomeraoplati
                        SET num = ? 
                        WHERE num = ?
                        """
                        data = (opa, int(opa - 1))
                        c.execute(sql, data)
                        conn.commit()
                        ajajaj = 10
                try:
                    ajajaj
                except:
                    msg = bot.send_message(message.chat.id,'Оплата не найдена!',reply_markup=markupopl3, parse_mode='html')
                    bot.register_next_step_handler(msg, balance5)
        except:
            bot.send_message(message.chat.id, '⛔️ ⛔️ Что-то пошло не так!',reply_markup=markup)
    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (int(message.chat.id),)
            c.execute('SELECT * FROM payments WHERE id=?', t)
            ax = c.fetchone()
            project_id = '5813'
            amount = str(ax[2])
            currency = 'RUB'
            pay_id = str(ax[1])
            secret_key = 'bVWgGA6EoEoHllo6Tql8yCj'
            arr_sign = bytes(f'{currency}:{amount}:{secret_key}:{project_id}:{pay_id}', encoding='utf-8')
            result = hashlib.md5(arr_sign)
            a = result.hexdigest()
            a = str(a)
            params = {'merchant_id': project_id, 'amount': amount, 'currency': currency, 'pay_id': pay_id, 'sign': a}
            r = requests.get('https://anypay.io/merchant', params=params)
            ek = str(r.url)
            msg = bot.send_message(message.chat.id,'Сумма: ' + str(ax[2]) + '\nПополнить баланс можно по ссылке ниже:\n' + str(ek),reply_markup=markupopl3, parse_mode='html')
            bot.register_next_step_handler(msg, balance5)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

def balance3(message):
    if message.text == '↩️ Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text == None:
        msg = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, balance3)
    elif message.text.isdigit() and int(message.text) > 4:
        try:
            g = int(message.text)
            f = int(message.chat.id)
            url = "https://qiwi.com/payment/form/99999?extra['account']="+str(nickname)+"&extra['comment']="+str(f)+"&amountInteger="+str(g)+"&amountFraction=0&currency=643&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"
            data = [int(message.from_user.id),f,g]
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute("INSERT INTO payments VALUES (?,?,?)",data)
            conn.commit()
            msg = bot.send_message(message.chat.id, 'Обязательно укажите комментарий к платежу!\n\nВаш комментарий: `'+str(f)+'`\n\nСумма: '+str(g)+'\n\nНельзя менять никакие данные, иначе платеж не зачислится автоматически\n\nЕсли поле никнейма оказалось пустым, введите туда "BOOSTME" (без кавычек)\n\nПополнить баланс можно по ссылке ниже:\n' + str(url),reply_markup=markupopl3, parse_mode='markdown')
            bot.register_next_step_handler(msg, balance4)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, balance3)

def balance4(message):
    if message.text == '↩️ Назад':
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            id = str(message.from_user.id)
            t = (id,)
            c.execute("""DELETE from payments where id = ?""", t)
            conn.commit()
            bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)
    elif message.text == '✅ Оплатил(a)':
        try:
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + qiwi_api_access_token
            parameters = {'rows': '20'}
            h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + phone_number + '/payments', params=parameters)
            req = json.loads(h.text)
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (int(message.chat.id),)
            c.execute('SELECT * FROM payments WHERE id=?', t)
            a = c.fetchone()
            if len(req['data']) == 0:
                bot.send_message(message.chat.id, 'Оплата не найдена', reply_markup=markupopl3)
            else:
                for i in range(len(req['data'])):
                    try:
                        int(req['data'][i]['comment'])
                    except:
                        continue
                    if int(req['data'][i]['comment']) == int(a[1]):
                        if int(req['data'][i]['sum']['amount']) == int(a[2]):
                            rng1 = random.randint(1, 1)
                            rng2 = random.uniform(0.1, 1)
                            zad_time = rng2 * rng1
                            time.sleep(zad_time)
                            t = (int(message.chat.id),)
                            c.execute("""DELETE from payments where id = ?""", t)
                            t = (int(message.chat.id),)
                            c.execute('SELECT * FROM users WHERE id=?', t)
                            g = c.fetchone()
                            b = float(g[1]) + float(a[2])
                            b = round(b, 2)
                            sql = """
                            UPDATE users
                            SET balance = ? 
                            WHERE id = ?
                            """
                            t = int(message.chat.id)
                            data = (b, t)
                            c.execute(sql, data)
                            conn.commit()
                            bot.send_message(message.chat.id, 'Оплата произведена успешно. Ваш новый баланс: ' + str(b) + '₽',reply_markup=markup)
                            conn = sqlite3.connect('example.db')
                            c = conn.cursor()
                            c.execute('SELECT * FROM nomeraoplati')
                            opa = c.fetchone()
                            opa = opa[0]
                            opa = int(opa)
                            opa = opa + 1
                            now = datetime.now()
                            current_time = now.strftime("%d.%m.%y в %H:%M")
                            bot.send_message(payment_group_id,"💰 Новая оплата #"+str(opa)+"\n\nСумма: "+str(a[2])+"₽"+"\nОплачено: qiwi\nКто оплатил: "+str(message.from_user.id)+"\nTelegram никнейм: @"+str(message.from_user.username)+"\nВремя: "+str(current_time))
                            sql = """
                            UPDATE nomeraoplati
                            SET num = ? 
                            WHERE num = ?
                            """
                            data = (opa, int(opa - 1))
                            c.execute(sql, data)
                            conn.commit()
                            c.execute('SELECT * FROM qiwi_stats')
                            loxa = c.fetchone()
                            plus = float(a[2])
                            new_data = []
                            for i in range(len(loxa)-1):
                                ora = int(plus) + int(loxa[i])
                                new_data.append(ora)
                            ora = int(loxa[4]) + 1
                            new_data.append(ora)
                            t = ((int(ora - 1)),)
                            c.execute("""DELETE from qiwi_stats where amount = ?""", t)
                            conn.commit()
                            c.execute("INSERT INTO qiwi_stats VALUES (?,?,?,?,?)", new_data)
                            conn.commit()
                            aajajajajajjaj = 10
                try:
                    aajajajajajjaj
                except:
                    msg = bot.send_message(message.chat.id,'Оплата не найдена!',reply_markup=markupopl3)
                    bot.register_next_step_handler(msg, balance4)
        except:
            msg = bot.send_message(message.chat.id, '⛔️ Что-то пошло не так! Пожалуйста, попробуйте еще раз или в другое время', reply_markup=markupopl3)
            bot.register_next_step_handler(msg, balance4)

    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (int(message.chat.id),)
            c.execute('SELECT * FROM payments WHERE id=?', t)
            a = c.fetchone()
            url = "https://qiwi.com/payment/form/99999?extra['account']=" + str(nickname) + "&extra['comment']=" + str(int(a[1])) + "&amountInteger=" + str(int(a[2])) + "&amountFraction=0&currency=643&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"
            msg = bot.send_message(message.chat.id, 'Обязательно укажите комментарий к платежу!\n\nВаш комментарий: ' + str(int(a[1])) + '\n\nСумма: ' + str(int(a[2])) + '\nНельзя менять никакие данные,иначе платеж не зачислится автоматически\n\nЕсли поле никнейма оказалось пустым, введите туда "BOOSTME" (без кавычек)\n\nОплатить баланс можно по ссылке ниже:\n' + str(url),reply_markup=markupopl3)
            bot.register_next_step_handler(msg, balance4)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📋 Мои задания")
def mytasls(message):
    try:
        if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
            bot.send_message(message.chat.id, 'Бот не работает в беседах')
        else:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (int(message.chat.id),)
            c.execute('SELECT * FROM zadania WHERE id=?', t)
            a = c.fetchall()
            if a == []:
                bot.send_message(message.chat.id, '⛔️ У вас пока нет активных заданий!', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Ваши активные задания:', reply_markup=markup)
                for i in range(len(a)):
                    bot.send_message(message.chat.id, 'Задание #'+str(a[i][6])+'\n\nСоциальная сеть: '+str(a[i][1])+'\nУслуга: '+str(a[i][2])+'\nКоличество: '+str(a[i][4])+'\nСсылка на задание: '+str(a[i][3])+'\nСумма: '+str(a[i][5])+'\nСтатус: Не выполнено\nДата и время: '+str(a[i][8]))
    except:
        bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📜 Правила")
def mytasls(message):
    try:
        if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
            bot.send_message(message.chat.id, 'Бот не работает в беседах')
        else:
            bot.send_message(message.chat.id, '1. Общее\n\n 1.1 Незнание правил не освобождает от ответственности.\n\n 1.2 Начав использовать бота Вы подтверждаете свое согласие с данными правилами.\n\n 1.3 Администрация не несет ответственности за временную или постоянную невозможность использования бота конкретным лицом или группой лиц.\n\n 1.4 Игроки обязаны выполнять требования Администрации и предписания данных правил.\n\n 1.5 Администрация имеет право корректировать данный свод правил без уведомления пользователя.\n\n 1.6 Администрация не несет ответственности за ваши аккаунты в социальных сетях.\n\n 1.7 Администрация не несет ответственности за возможное списание услуг (лайки, подписчики, друзья и т.д).\n\n2. Аккаунт\n\n 2.1 Администрация имеет право блокировать/обнулять аккаунт по собственному желанию, без причины.\n\n 2.2 Администрация не обязана предоставлять доказательства на блокировку/обнуление аккаунтов.\n\n 2.3 Администрация имеет право обнулять аккаунты пользователей, не посещавших бота более 100 дней.\n\n 2.4 Ответственность несет владелец аккаунта, независимо от того, кто совершал действия под данным аккаунтом.\n\n 2.5 Запрещено присылать в репорт/в поддержку (@boost_me_support) рекламу, оскорбления, спам.\n\n ⛔️ Наказание: блокировка возможности писать в репорт на срок по усмотрению администрации.\n\nЕсли Вы нашли баг, или у вас есть вопрос по боту, обратитесь в репорт. Если у Вас есть деловые предложения, обратитесь к агенту поддержки @boost_me_support\n\nПриятного использования ❤️', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "✉️ Репорт")
def report(message):
    if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
        bot.send_message(message.chat.id, 'Бот не работает в беседах')
    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (int(message.chat.id),)
            c.execute('SELECT * FROM banlist WHERE id = ?',t)
            fo = c.fetchone()
            if not fo == None:
                ban_time = fo[2]
                now_time = datetime.now().timestamp()
                rem_time = int(ban_time) - int(now_time)
                rem_time = int(rem_time)
                m, s = divmod(rem_time, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                mn, d = divmod(d, 30)
                y, mn = divmod(mn, 12)
                if int(y) == 1:
                    remain_time = "%dгод:%dмес:%dдн:%dч:%dмин:%dсек" % (y,mn,d,h, m, s)
                elif int(y) == 2 or int(y) == 3 or int(y) == 4:
                    remain_time = "%dгода:%dмес:%dдн:%dч:%dмин:%dсек" % (y,mn,d,h, m, s)
                else:
                    remain_time = "%dлет:%dмес:%dдн:%dч:%dмин:%dсек" % (y,mn,d,h, m, s)
                bot.send_message(message.chat.id, "Вам заблокирована возможность писать репорты\n\nДо разблокировки: "+str(remain_time), reply_markup=markup)
            else:
                try:
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    t = (int(message.chat.id),)
                    c.execute('SELECT * FROM reports WHERE status = ?', t)
                    fo = c.fetchone()
                    if fo == None:
                        msg = bot.send_message(message.chat.id, "Введите сообщение для администрации:", reply_markup=markupnazad)
                        bot.register_next_step_handler(msg, nnn)
                    else:
                        bot.send_message(message.chat.id, "⛔️ Дождитесь ответа администрации!", reply_markup=markup)
                except:
                    bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

def nnn(message):
    try:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT * FROM reporti')
        a = c.fetchone()
        a = int(a[0])
        a = a + 1
        if message.text == '↩️ Назад':
            bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
        else:
            if len(str(message.text)) < 10:
                msg = bot.send_message(message.chat.id, "Репорт только от 10 символов!", reply_markup=markupnazad)
                bot.register_next_step_handler(msg, nnn)
            else:
                bot.send_message(message.chat.id, "Ваше сообщение отправлено", reply_markup=markup)
                now = datetime.now()
                current_time = now.strftime("%d.%m.%y в %H:%M")
                msg = bot.send_message(group_id, '🔔 Новый репорт #'+str(a)+'\n\nКто написал: '+str(message.chat.id)+'\nТелеграмм никнейм: @'+str(message.from_user.username)+'\nДата и время: '+str(current_time)+'\n\nТекст репорта: '+str(message.text))
                sql = """
                UPDATE reporti
                SET id = ? 
                WHERE id = ?
                """
                data = (a, int(a-1))
                c.execute(sql, data)
                conn.commit()
                data = [str(msg.text),int(message.chat.id)]
                c.execute('INSERT INTO reports VALUES (?,?)', data)
                conn.commit()
    except:
        bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin(message):
    global markupadmin
    markupadmin = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рассылка")
    item2 = types.KeyboardButton("Купон")
    markupadmin.add(item1,item2,btn0)
    if message.chat.id == group_id or message.chat.id == payment_group_id or message.chat.id == task_group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            t = (message.chat.id,)
            c.execute('SELECT * FROM Users WHERE id=?', t)
            a = c.fetchone()
            if int(a[2]) == 1:
                msg = bot.send_message(message.chat.id, 'Меню администратора', reply_markup=markupadmin)
                bot.register_next_step_handler(msg, admin2)
            else:
                bot.send_message(message.chat.id, 'У вас нет прав администратора', reply_markup=markup)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

def admin2(message):
    if message.text == "Рассылка":
        msg = bot.send_message(message.chat.id, 'Введите ваше сообщение:', reply_markup=markupnazad)
        bot.register_next_step_handler(msg, rassilka)
    elif message.text == '↩️ Назад':
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
    elif message.text == "Купон":
        params = {'api_token':api_token}
        r = requests.get('https://vkmix.com/api/2/getBalance', params=params)
        n = r.json()
        msg = bot.send_message(message.chat.id, 'Текущий баланс: '+str(n['response']),reply_markup=markupkupon)
        bot.register_next_step_handler(msg, vvestik)

def vvestik(message):
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Меню администратора', reply_markup=markupadmin)
        bot.register_next_step_handler(msg, admin2)
    elif message.text == 'Ввести купон':
        msg = bot.send_message(message.chat.id, 'Введите код купона:',reply_markup=markupnazad)
        bot.register_next_step_handler(msg, lod)
    else:
        msg = bot.send_message(message.chat.id, 'Текущий баланс: ' + str(n['response']), reply_markup=markupkupon)
        bot.register_next_step_handler(msg, vvestik)

def lod(message):
    a = str(message.text)
    params = {'api_token': api_token,'code':a}
    r = requests.get('https://vkmix.com/i/coupons/activate?', params=params)
    n = r.text
    if n.startswith('{"error"'):
        msg = bot.send_message(message.chat.id, 'Не верный код купона', reply_markup=markupadmin)
        bot.register_next_step_handler(msg, admin2)
    else:
        msg = bot.send_message(message.chat.id, 'Купон успешно активирован', reply_markup=markupadmin)
        bot.register_next_step_handler(msg, admin2)

def rassilka(message):
    if message.text == '↩️ Назад':
        msg = bot.send_message(message.chat.id, 'Меню администратора', reply_markup=markupadmin)
        bot.register_next_step_handler(msg, admin2)
    else:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users')
            m = c.fetchall()
            try:
                for i in range (len(m)):
                    try:
                        bot.send_message(m[i][0], message.text)
                    except:
                        continue
                msg = bot.send_message(message.chat.id, 'Рассылка успешно отправлена',reply_markup=markupadmin)
                bot.register_next_step_handler(msg, admin2)
            except:
                msg = bot.send_message(message.chat.id, 'Рассылка отправлена неуспешно!\nБот не нашел какой-то чат!', reply_markup=markupadmin)
                bot.register_next_step_handler(msg, admin2)
        except:
            bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def xz(message):
    try:
        bantime = {
            'сек': '1',
            'мин':'60',
            'час':'3600',
            'нед': '86400',
            'мес': '2678400',
            'год': '32140800',
        }
        if message.chat.id == group_id:
            if str(message.text).startswith('Бан') or str(message.text).startswith('бан') or str(message.text).startswith('ban') or str(message.text).startswith('Ban'):
                eko = str(message.text)
                a = eko.split(' ')
                try:
                    a = message.json['reply_to_message']['text']
                    f = a.split('\n')
                    f = f[1]
                    f = f[12:]
                    fax = int(f)
                    bot.send_message(fax,'Вам заблокирована возможность писать репорты')
                    bot.send_message(group_id,'Выдал блокировку')
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    now = datetime.now()
                    bandate = datetime.timestamp(now)
                    a = eko.split(' ')
                    f = a[1]
                    e = a[2]
                    bantimes = int(bantime[str(e)]) * int(f)
                    banend = int(bandate) + int(bantimes)
                    data = [int(fax),bandate,banend,bantimes]
                    try:
                        t = (int(fax),)
                        c.execute("""DELETE from banlist where id = ?""", t)
                        conn.commit()
                    except:
                        pass
                    finally:
                        c.execute('INSERT OR IGNORE INTO banlist VALUES (?,?,?,?)',data)
                        conn.commit()
                except Exception as E:
                    try:
                        a = eko.split(' ')
                        f = a[1]
                        e = a[2]
                        g = a[3]
                        bot.send_message(int(f), 'Вам заблокирована возможность писать репорты')
                        bot.send_message(group_id, 'Выдал блокировку')
                        conn = sqlite3.connect('example.db')
                        c = conn.cursor()
                        now = datetime.now()
                        bandate = datetime.timestamp(now)
                        bantimes = int(bantime[str(g)]) * int(e)
                        banend = int(bandate) + int(bantimes)
                        data = [int(f), bandate, banend, bantimes]
                        try:
                            t = (int(f),)
                            c.execute("""DELETE from banlist where id = ?""", t)
                            conn.commit()
                        except:
                            pass
                        finally:
                            c.execute('INSERT OR IGNORE INTO banlist VALUES (?,?,?,?)', data)
                            conn.commit()
                    except Exception as E:
                        bot.send_message(group_id, '⛔️ Что-то пошло не так!')
            elif message.text == "Бвсе":
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                c.execute('SELECT * FROM users')
                auf = c.fetchall()
                esum = 0
                for i in range(len(auf)):
                    esum = esum + auf[i][1]
                bot.send_message(group_id, 'Всего у пользователей: '+str(esum) + ' ₽')
            elif message.text == "Рвсе":
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                c.execute('SELECT * FROM reports')
                auf = c.fetchall()
                if auf == []:
                    bot.send_message(group_id, 'Все репорты отвечены!')
                else:
                    bot.send_message(group_id, 'Все неотвеченные репорты:')
                    for i in range(len(auf)):
                        bot.send_message(group_id, auf[i][0])
            elif str(message.text).startswith('setbalance'):
                try:
                    ept = str(message.text)
                    ept = ept.split(' ')
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    t = ((int(ept[1])),)
                    c.execute('SELECT * FROM users WHERE id = ?',t)
                    auf = c.fetchone()
                    if auf == None:
                        bot.send_message(group_id, 'Пользователь не найден!\nПроверьте правильность введенного id!')
                    else:
                        a = int(ept[2])
                        sql = """
                        UPDATE users
                        SET balance = ? 
                        WHERE id = ?
                        """
                        data = (a, int(auf[0]))
                        c.execute(sql, data)
                        conn.commit()
                        bot.send_message(group_id, 'Пользователь: ' + str(auf[0]) + '\nНовый баланс: ' + str(a) + ' р')
                except:
                    bot.send_message(group_id, '⛔️ Что-то пошло не так!\nПроверь правильность введенных данных!')
            elif str(message.text).startswith('checkbalance'):
                try:
                    ept = str(message.text)
                    ept = ept.split(' ')
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    t = ((int(ept[1])),)
                    c.execute('SELECT * FROM users WHERE id = ?', t)
                    auf = c.fetchone()
                    if auf == None:
                        bot.send_message(group_id, 'Пользователь не найден!\nПроверьте правильность введенного id!')
                    else:
                        bot.send_message(group_id, 'Пользователь: ' + str(auf[0]) + '\nБаланс: ' + str(auf[1]) + ' р')
                except:
                    bot.send_message(group_id, '⛔️ Что-то пошло не так!\nПроверь правильность введенных данных!')
            else:
                try:
                    a = message.json['reply_to_message']['text']
                    f = f = a.split('\n')
                    f = f[2]
                    f = f[12:]
                    f = int(f)
                    bot.send_message(f, '🔔 Вам пришел ответ от администрации: ' + str(message.text))
                    bot.send_message(message.chat.id, 'Ответ успешно отправлен')
                    t = (message.json['reply_to_message']['text'],)
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    c.execute("""DELETE from reports where text = ?""", t)
                    conn.commit()
                except:
                    pass
        elif message.chat.id == payment_group_id:
            if str(message.text) == 'Кстат':
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                c.execute('SELECT * FROM qiwi_stats')
                f = c.fetchone()
                bot.send_message(payment_group_id, 'За сегодня: '+str(f[0])+' р\nЗа неделю: '+str(f[1])+' р\nЗа месяц: '+str(f[2])+' р\nВсего: '+str(f[3])+' р\nКол-во пополнений: '+str(f[4]))
            else:
                pass
        elif message.chat.id == task_group_id:
            pass
        else:
            bot.send_message(message.chat.id, 'Такой команды не существует')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, '⛔️ Что-то пошло не так!', reply_markup=markup)

def doubler():
    while True:
        try:
            params = {'api_token': api_token}
            r = requests.get('https://vkmix.com/api/2/getBalance', params=params)
            a = r.json()['response']
            a = int(a)
            if a == 0 or a is bool:
                time.sleep(300)
            elif a < 1000:
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                c.execute('SELECT * FROM users')
                o = c.fetchall()
                bot.send_message(group_id, 'Предупреждение о низком балансе! Текущий баланс составляет: ' + str(a))
                #for i in range(len(o)):
                    #if int(o[i][2]) == 1:
                        #bot.send_message(int(o[i][0]),'Предупреждение о низком балансе! Текущий баланс составляет: ' + str(a))
                time.sleep(1800)
            else:
                time.sleep(1800)
        except:
            time.sleep(1800)
            continue

def tripler_three():
    while True:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM zadania')
            e = c.fetchall()
            if e == []:
                time.sleep(300)
            else:
                for i in range(len(e)):
                    b = int(e[i][7])
                    params = {'api_token': api_token, 'id': b}
                    r = requests.get('https://vkmix.com/api/2/getTasks', params=params)
                    a = r.json()["response"]['items'][0]['status']
                    if str(a) == 'success':
                        bot.send_message(e[i][0], "✅ Задание под номером #"+str(int(e[i][6]))+" успешно выполнено!")
                        t = (int(e[i][6]),)
                        c.execute("""DELETE from zadania where primirary_id = ?""", t)
                        conn.commit()
                time.sleep(300)
        except:
            time.sleep(300)

def unban():
    while True:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM banlist')
            ajj = c.fetchall()
            for el in ajj:
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                if int(el[2]) <= int(timestamp):
                    t = (int(el[0]),)
                    c.execute("""DELETE from banlist where id = ?""", t)
                    conn.commit()
                    bot.send_message(int(el[0]), 'Вам возвращена возможность писать репорты')
                else:
                    continue
        except:
            continue

def nuller():
    while True:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM qiwi_stats')
            f = c.fetchone()
            now = datetime.now()
            a = now.strftime('%H:%M')
            a = str(a)
            if a == '08:00' or a == '08:01' or a == '08:02' or a == '08:03' or a == '08:04' or a == '08:05':
                sql = """
                UPDATE qiwi_stats
                SET today = ? 
                WHERE today = ?
                """
                data = (int(0), int(f[0]))
                c.execute(sql, data)
                conn.commit()
            b = now.strftime('%A')
            if str(b) == 'Monday' and a == '08:00' or a == '08:01' or a == '08:02' or a == '08:03' or a == '08:04' or a == '08:05':
                sql = """
                UPDATE qiwi_stats
                SET week = ? 
                WHERE week = ?
                """
                data = (int(0), int(f[1]))
                c.execute(sql, data)
                conn.commit()
            v = now.strftime('%d')
            if str(v) == '01' and a == '08:00' or a == '08:01' or a == '08:02' or a == '08:03' or a == '08:04' or a == '08:05':
                sql = """
                UPDATE qiwi_stats
                SET months = ? 
                WHERE months = ?
                """
                data = (int(0), int(f[2]))
                c.execute(sql, data)
                conn.commit()
        except:
            continue

def task_status_chng():
    while True:
        try:
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM tasks_status')
            f = c.fetchall()
            for i in range(len(f)):
                params = {'api_token': api_token, 'id': int(f[i][2])}
                r = requests.get('https://vkmix.com/api/2/getTasks', params=params)
                #a = r.json()["response"]['items'][0]['done_count']
                #eptaaa = str(f[i][1])
                #af = eptaaa.rfind('0')
                #text = eptaaa[:af] + str(a) + eptaaa[af + 1:]
                try:
                    #bot.edit_message_text(chat_id=task_group_id, message_id=int(f[i][0]), text=str(text))
                    e = r.json()["response"]['items'][0]['status']
                    if str(e) == 'success':
                        text = str(f[i][1])
                        text = text.replace('Не выполнен','Выполнен')
                        bot.edit_message_text(chat_id=task_group_id, message_id=int(f[i][0]), text=str(text))
                        t = (int(f[i][2]),)
                        c.execute("""DELETE from tasks_status where task_id = ?""", t)
                        conn.commit()
                    else:
                        continue
                except:
                    continue
        except:
            continue

if __name__ == '__main__':
    my_thread1 = threading.Thread(target=doubler)
    my_thread1.start()
    my_thread2 = threading.Thread(target=tripler_three)
    my_thread2.start()
    my_thread3 = threading.Thread(target=unban)
    my_thread3.start()
    my_thread4 = threading.Thread(target=nuller)
    my_thread4.start()
    my_thread5 = threading.Thread(target=task_status_chng)
    my_thread5.start()
    bot.polling(none_stop=True, timeout=999999)
