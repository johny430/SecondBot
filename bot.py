import telebot
from telebot import types
import json
import requests
import sqlite3
import threading
import random
import time
from datetime import datetime
import hashlib

bot = telebot.TeleBot('1170679484:AAGB64C0BTQi7NvCQSIs1uO2O6wGrtSgBQM')
api_token = 'emOVGMKUKWLUIyiFqBnaRDhIVJHxrIHchLVwjITaXODFVvFEMp'
group_id = -1001151029976
coef = 0.036
qiwi_api_access_token = '1c01bd50dd0e80531378cae9fb06c895'
phone_number = '+375444734398'
nickname = ''

jsan = {
    'ВКонтакте': {
        'Лайки': 2,
        'Участники': 4,
        'Друзья': 4,
        'Репосты': 4,
        'Голоса в опросе': 2,
    },
    'Ютуб': {
        'Лайки': 6,
        'Подписчики': 6,
        'Дизлайки': 5,
        'Лайки на  комментарий': 2,
    },
    'Инстаграмм': {
        'Лайки': 2,
        'Подписчики': 4,
        'Лайки на  комментарий': 2,
    },
    'Телеграм': {
        'Подписчики': 4,
    },
    'Одноклассники': {
        'Классы': 3,
        'Друзья': 3,
        'Подписчики': 3,
    },
    'Твиттер': {
        'Ретвиты': 5,
        'Фолловеры': 5,
        'Лайки': 5,
},
}

forapi = {
    'ВКонтакте': {
        'Лайки': "likes",
        'Участники': 'groups',
        'Друзья': 'friends',
        'Репосты': "reposts",
        'Голоса в опросе': "polls",
    },
    'Ютуб': {
        'Лайки': "likes",
        'Подписчики': 6,
        'Дизлайки': 'dislikes',
        'Лайки на  комментарий': "comments_likes",
    },
    'Инстаграмм': {
        'Лайки': "likes",
        'Подписчики': 'subscribers',
        'Лайки на  комментарий': "comments_likes",
    },
    'Телеграм': {
        'Подписчики': 'subscribers',
    },
    'Одноклассники': {
        'Классы': "likes",
        'Друзья': "friends",
        'Подписчики': 'groups',
    },
    'Твиттер': {
        'Ретвиты': "retweets",
        'Фолловеры': "followers",
        'Лайки': "favorites",
},
}

speeds = {
    'ВКонтакте':{
        'Лайки':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
            },
        'Друзья':{
            'Обычный' : 4,
            'Быстрый' : 6,
        },
        'Репосты':{
            'Обычный': 4,
            'Быстрый' : 6,
            },
        'Участники':{
            'Обычный': 4,
            'Быстрый' : 7,
        },
        'Голоса в опросе':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
        },
    },
    'Инстаграмм':{
        'Лайки':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
        },
        'Подписчики':{
            'Обычный' : 4,
            'Быстрый' : 7,
        },
        'Лайки на  комментарий':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
        },
    },
    'Ютуб':{
        'Лайки':{
            'Обычный' : 6,
            'Быстрый' : 9,
    },
        'Дизлайки':{
            'Обычный' : 5,
            'Быстрый' : 10,
    },
        'Подписчики':{
            'Обычный' : 6,
            'Быстрый' : 9,
    },
        'Лайки на  комментарий':{
            'Обычный' : 2,
            'Быстрый' : 4,
            'Очень быстрый' : 6,
},
    },
    'Телеграм':{
        'Подписчики':{
            'Обычный' : 4,
            'Быстрый' : 7,
        },
},
    'Одноклассники':{
        'Классы':{
            'Обычный' : 3,
            'Быстрый' : 6,
        },
        'Друзья':{
            'Обычный' : 3,
            'Быстрый' : 6,
        },
        'Подписчики':{
            'Обычный' : 3,
            'Быстрый' : 6,
        },
},
    'Твиттер':{
        'Ретвиты':{
            'Обычный' : 5,
            'Быстрый' : 10,
        },
        'Фолловеры':{
            'Обычный' : 5,
            'Быстрый': 10,
        },
        'Лайки':{
            'Обычный' : 5,
            'Быстрый' : 10,
        },
},
}

sootv = {"ВКонтакте": "vk", "Телеграм": "telegram", "Инстаграмм": "instagram", "Твиттер": "twitter","Одноклассники": "ok", "Ютуб": "youtube"}

markupkupon = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn0 = types.KeyboardButton("Назад")
item10 = types.KeyboardButton("Ввести купон")
markupkupon.add(btn0, item10)

markupopl2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn0 = types.KeyboardButton("Назад")
pppl = types.KeyboardButton("Пополнить")
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
item111 = types.KeyboardButton("Оплатил(a)")
markupopl3.add(item111,btn0)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn1 = types.KeyboardButton("Накрутить")
btn2 = types.KeyboardButton("Баланс")
btn3 = types.KeyboardButton("Репорт")
markup.add(btn1, btn2, btn3)

btn_2 = types.KeyboardButton("Дизлайки")
btn_1 = types.KeyboardButton("Участники")
btn1 = types.KeyboardButton("Лайки")
btn2 = types.KeyboardButton("Друзья")
btn3 = types.KeyboardButton("Репосты")
btn4 = types.KeyboardButton("Комментарии")
btn5 = types.KeyboardButton("Голоса в опросе")
btn6 = types.KeyboardButton("Подписчики")
btn7 = types.KeyboardButton("Лайки на  комментарий")
btn8 = types.KeyboardButton("Дизлайки")
btn9 = types.KeyboardButton("Друзья")
btn10 = types.KeyboardButton("Классы")
btn11 = types.KeyboardButton("Ретвиты")
btn12 = types.KeyboardButton("Фолловеры")
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
anypay = types.KeyboardButton('AnyPay (остальные платежные системы)')
qiwis = types.KeyboardButton('Qiwi')
markupchtos.add(anypay,qiwis,btn0)

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id == group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        dannie = [int(message.from_user.id),float(0),int(1)]
        c.execute("INSERT OR IGNORE INTO Users VALUES (?,?,?)", dannie)
        conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Накрутить")
def krt(message):
    if message.chat.id == group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)

def chto(message):
    global b
    b = str(message.text)
    if message.text == "ВКонтакте":
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=vk)
        bot.register_next_step_handler(msg, next)
    elif message.text == 'Телеграм':
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=tg)
        bot.register_next_step_handler(msg, teg)
    elif message.text == 'Инстаграмм':
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=inst)
        bot.register_next_step_handler(msg, insta)
    elif message.text == 'Твиттер':
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=twt)
        bot.register_next_step_handler(msg, twter)
    elif message.text == 'Одноклассники':
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=odnkl)
        bot.register_next_step_handler(msg, odnoklas)
    elif message.text == 'Ютуб':
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=youtube)
        bot.register_next_step_handler(msg, youtab)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)

def next(message):
    global e,x
    x = b
    e = str(message.text)
    spisok1 = ["Лайки", "Друзья", "Репосты","Участники"]
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    elif str(message.text) == "Голоса в опросе":
        msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, nextvk)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=vk)
        bot.register_next_step_handler(msg, next)

def nextvk(message):
    global o
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
    elif message.text.isdigit():
        if int(message.text) > 0:
            o = int(message.text)
            msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:", reply_markup=markupnazad)
            bot.register_next_step_handler(msg, next2)
        else:
            msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:",reply_markup=markupnazad)
            bot.register_next_step_handler(msg, nextvk)
    else:
        msg = bot.send_message(message.chat.id, "Введите номер пункта, за который нужно проголосовать:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, nextvk)

def teg(message):
    global e, x
    x = b
    e = str(message.text)
    spisok1 = ["Подписчики"]
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выбери куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выбери что нужно накрутить:', reply_markup=tg)
        bot.register_next_step_handler(msg, teg)

def insta(message):
    global e, x
    x = b
    e = str(message.text)
    spisok1 = ["Лайки","Подписчики","Лайки на  комментарий"]
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=inst)
        bot.register_next_step_handler(msg, insta)

def twter(message):
    global e, x
    x = b
    e = str(message.text)
    spisok1 = ["Лайки","Фолловеры","Ретвиты"]
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=twt)
        bot.register_next_step_handler(msg, twter)

def odnoklas(message):
    global e, x
    x = b
    e = str(message.text)
    spisok1 = ["Подписчики","Классы","Друзья"]
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        msg = bot.send_message(message.chat.id, "Введите ссылку куда нужно произвести накрутку:",reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=odnkl)
        bot.register_next_step_handler(msg, odnoklas)

def youtab(message):
    global e, x
    x = b
    e = str(message.text)
    spisok1 = ["Подписчики","Лайки","Лайки на  комментарий","Дизлайки"]
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Выберите куда нужно произвести накрутку:', reply_markup=kuda)
        bot.register_next_step_handler(msg, chto)
    elif str(message.text) in spisok1:
        msg = bot.send_message(message.chat.id, 'Введите ссылку куда нужно произвести накрутку:',reply_markup=markupnazad)
        bot.register_next_step_handler(msg, next2)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите что нужно накрутить:', reply_markup=youtube)
        bot.register_next_step_handler(msg, youtab)

def next2(message):
    global g
    g = str(message.text)
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, "Выберите количество:",reply_markup=markupnone)
        bot.register_next_step_handler(msg, next3)

def next3(message):
    global q, l, aloxa, kaaaaa
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    elif message.text.isdigit():
        if int(message.text) < 5:
            msg = bot.send_message(message.chat.id, "Минимально 5\n\nУкажите верное количество:", reply_markup=markupnone)
            bot.register_next_step_handler(msg, next3)
        elif int(message.text) >= 2000:
            q = int(message.text)
            markupSPEED = types.ReplyKeyboardMarkup(row_width=1)
            aloxa = list(speeds[x][e])
            for i in range(len(aloxa)):
                atatat = types.KeyboardButton(str(aloxa[i]))
                markupSPEED.add(atatat)
            markupSPEED.add(btn0)
            msg = bot.send_message(message.chat.id, "Хорошо, выберите режим скорости:",reply_markup=markupSPEED)
            bot.register_next_step_handler(msg, rejim)
        else:
            q = int(message.text)
            f = int(jsan[b][e])
            l = f * q * coef
            kaaaaa = 'Обычный'
            msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - "+str(l)+"₽",reply_markup=markupopl)
            bot.register_next_step_handler(msg, next4)
    else:
        msg = bot.send_message(message.chat.id, "Введите количество:", reply_markup=markupnone)
        bot.register_next_step_handler(msg, next3)

def rejim(message):
    global l, kaaaaa
    aloxa = list(speeds[x][e])
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif str(message.text) in aloxa:
        f = int(jsan[b][e])
        kaaaaa = str(message.text)
        if message.text == 'Обычный':
            kaaaaa = str(message.text)
            l = f * q * coef
            msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - " + str(l) + "₽",reply_markup=markupopl)
            bot.register_next_step_handler(msg, next4)
        elif message.text == 'Быстрый':
            kaaaaa = str(message.text)
            l = f * q * coef * 2
            msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - " + str(l) + "₽",reply_markup=markupopl)
            bot.register_next_step_handler(msg, next4)
        elif message.text == 'Очень быстрый':
            kaaaaa = str(message.text)
            l = f * q * coef * 3
            msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - " + str(l) + "₽",reply_markup=markupopl)
            bot.register_next_step_handler(msg, next4)
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
    s = q
    kaaaaas = kaaaaa
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text == 'Оплатить':
        try:
            o
            data = [int(message.from_user.id),x,e,g,s,l,o]
        except:
            data = [int(message.from_user.id),x, e, g, s, l]
        try:
            kaaaaas
        except:
            kaaaaas = 'Обычный'
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = int(message.chat.id)
        t =(t,)
        c.execute('SELECT * FROM users WHERE id=?', t)
        a = c.fetchone()
        if int(a[1]) < l:
            bot.send_message(message.chat.id, 'Для накрутки не достаточно средств\n\nПополнить баланс можно в главном меню',reply_markup=markup)
        else:
            if len(data) == 6:
                a = sootv[data[1]]
                p = forapi[data[1]][data[2]]
                c = data[3]
                d = data[4]
                f = data[5]
                pl = speeds[data[1]][data[2]][kaaaaas]
                data2 = [int(message.from_user.id),a,p,c,d,f]
                params = {'api_token': api_token, 'network': a,'section': p,'link': c,'count': q, 'amount': pl}
                r = requests.get('https://vkmix.com/api/2/createTask', params=params)
                r = r.text
                if r.startswith('{"error":'):
                    bot.send_message(message.chat.id, 'Мне не удалось создать задание',reply_markup=markup)
                else:
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    t = int(message.chat.id)
                    t = (t,)
                    c.execute('SELECT * FROM users WHERE id=?', t)
                    a = c.fetchone()
                    pox = float(a[1])
                    b = pox - float(l)
                    sql = """
                    UPDATE users
                    SET balance = ? 
                    WHERE id = ?
                    """
                    data = (b, int(message.from_user.id))
                    c.execute(sql, data)
                    conn.commit()
                    c.execute('SELECT * FROM zadania')
                    alalal = c.fetchall()
                    ofaa = int(len(alalal))
                    ofaa = ofaa + 1
                    c.execute('SELECT * FROM nomezad')
                    apchu = c.fetchone()
                    apchu = int(apchu[0])
                    apchu = apchu + 1
                    data2.append(apchu)
                    bot.send_message(message.chat.id, 'Заказ успешно принят, после его выполнения я напишу вам',reply_markup=markup)
                    c.execute("INSERT INTO zadania VALUES (?,?,?,?,?,?,?)",data2)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M %d.%m.%y")
                    bot.send_message(group_id, 'Создано новое задание #' + str(apchu) + '\n\nКто создал: ' + str(message.from_user.id) + '\nTelegram ник: @' + str(message.from_user.username) + '\nКакая соц.сеть выбрана: ' + str(x) + '\nЧто выбрано для накрутки: ' + str(e) + '\nКоличество: ' + str(s) + '\nСумма: ' + str(l) + "₽" + '\nВремя: ' + str(current_time))
                    sql = """
                    UPDATE nomezad
                    SET num = ? 
                    WHERE num = ?
                    """
                    data = (apchu, int(apchu - 1))
                    c.execute(sql, data)
                    conn.commit()
            else:
                a = sootv[data[1]]
                p = forapi[data[1]][data[2]]
                c = data[3]
                d = data[4]
                f = data[5]
                pl = speeds[data[1]][data[2]][kaaaaas]
                data2 = [int(message.from_user.id), a, p, c, d, f]
                params = {'api_token': api_token, 'network': a,'section': p,'link': c,'count': q, 'amount': pl,'poll':o}
                r = requests.get('https://vkmix.com/api/2/createTask', params=params)
                r = r.text
                if r.startswith('{"error":'):
                    bot.send_message(message.chat.id, 'Мне не удалось создать задание',reply_markup=markup)
                else:
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    c.execute('SELECT * FROM nomezad')
                    apchu = c.fetchone()
                    apchu = int(apchu[0])
                    apchu = apchu + 1
                    sql = """
                    UPDATE nomezad
                    SET num = ? 
                    WHERE num = ?
                    """
                    data = (apchu, int(apchu - 1))
                    c.execute(sql, data)
                    conn.commit()
                    conn = sqlite3.connect('example.db')
                    c = conn.cursor()
                    t = int(message.chat.id)
                    t = (t,)
                    c.execute('SELECT * FROM users WHERE id=?', t)
                    a = c.fetchone()
                    pox = float(a[1])
                    b = pox - float(l)
                    sql = """
                    UPDATE users
                    SET balance = ? 
                    WHERE id = ?
                    """
                    data = (b, int(message.from_user.id))
                    c.execute(sql, data)
                    conn.commit()
                    c.execute('SELECT * FROM zadania')
                    alalal = c.fetchall()
                    ofaa = int(len(alalal))
                    ofaa = ofaa + 1
                    data2.append(apchu)
                    bot.send_message(message.chat.id, 'Заказ успешно принят, после его выполнения я напишу вам',reply_markup=markup)
                    c.execute("INSERT INTO zadania VALUES (?,?,?,?,?,?,?)", data2)
                    conn.commit()
                    now = datetime.now()
                    current_time = now.strftime("%H:%M %d.%m.%y")
                    bot.send_message(group_id, 'Создано новое задание #' + str(apchu) + '\n\nКто создал: ' + str(message.from_user.id) + '\nTelegram ник: @' + str(message.from_user.username) + '\nКакая соц.сеть выбрана: ' + str(x) + '\nЧто выбрано для накрутки: ' + str(e) + '\nКоличество: ' + str(s) + '\nСумма: ' + str(l) + '\nВремя: ' + str(current_time))
    else:
        msg = bot.send_message(message.chat.id, "Хорошо, сумма для оплаты - "+str(l)+"₽",reply_markup=markupopl)
        bot.register_next_step_handler(msg, next4)

@bot.message_handler(func=lambda message: message.text == "Баланс")
def balance(message):
    global  markupchto
    markupchto = types.ReplyKeyboardMarkup(row_width = 1)
    anypay = types.KeyboardButton('AnyPay (остальные платежные системы)')
    qiwis = types.KeyboardButton('Qiwi')
    markupchto.add(anypay,qiwis,btn0)
    if message.chat.id == group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
        global  a
        a = int(message.from_user.id)
        t = (a,)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id=?', t)
        a = c.fetchone()
        msg = bot.send_message(message.chat.id, "Ваш баланс: "+str(a[1])+" ₽\nПополнять нельзя ,так как это демонстрационный бот!\nМожно подключить любые методы оплаты!")#,reply_markup=markupopl2)
        #bot.register_next_step_handler(msg, balance2)

def balance2(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    elif message.text == "Пополнить":
        msg = bot.send_message(message.chat.id, "Выберите платежную систему:", reply_markup=markupchto)
        bot.register_next_step_handler(msg, chtos)
    else:
        msg = bot.send_message(message.chat.id, "Ваш баланс: " + str(a[1]) + "₽", reply_markup=markupopl2)
        bot.register_next_step_handler(msg, balance2)

def chtos(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:',reply_markup=markup)
    elif message.text  == 'AnyPay (остальные платежные системы)':
        msg2 = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg2, anypays)
    elif message.text  == 'Qiwi':
        msg4 = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg4, balance3)
    else:
        msg = bot.send_message(message.chat.id, "Выберите платежную систему:", reply_markup=markupchto)
        bot.register_next_step_handler(msg, chtos)

def anypays(message):
    global yes
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text.isdigit() and int(message.text) > 4:
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
    else:
        msg = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, anypays)

def balance5(message):
    if message.text == 'Назад':
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        id = str(message.from_user.id)
        t = (id,)
        c.execute("""DELETE from payments where id = ?""", t)
        conn.commit()
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text == 'Оплатил(a)':
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
                        a = int(yes)
                        t = (int(message.chat.id),)
                        c.execute("""DELETE from payments where id = ?""", t)
                        t = (int(message.chat.id),)
                        c.execute('SELECT * FROM users WHERE id=?', t)
                        g = c.fetchone()
                        b = float(g[1]) + float(a)
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
                        current_time = now.strftime("%H:%M %d.%m.%y")
                        bot.send_message(group_id, "Новая оплата #" + str(opa) + "\n\nСумма: " + str(a) + "₽" + "\nОплачено: AnyPay\nКто оплатил: " + str(message.from_user.id) + "\nTelegram никнейм: @" + str(message.from_user.username) + "\nВремя: " + str(current_time))
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
            bot.send_message(message.chat.id, 'Что-то пошло не так!',reply_markup=markup)
    else:
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

def balance3(message):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text.isdigit() and int(message.text) > 4:
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
    else:
        msg = bot.send_message(message.chat.id, "На сколько рублей хотите пополнить? (от 5₽)", reply_markup=markupnazad)
        bot.register_next_step_handler(msg, balance3)

def balance4(message):
    if message.text == 'Назад':
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        id = str(message.from_user.id)
        t = (id,)
        c.execute("""DELETE from payments where id = ?""", t)
        conn.commit()
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Выберите действие:', reply_markup=markup)
    elif message.text == 'Оплатил(a)':
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
                            t = (int(message.chat.id),)
                            c.execute("""DELETE from payments where id = ?""", t)
                            t = (int(message.chat.id),)
                            c.execute('SELECT * FROM users WHERE id=?', t)
                            g = c.fetchone()
                            b = float(g[1]) + float(a[2])
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
                            current_time = now.strftime("%H:%M %d.%m.%y")
                            bot.send_message(group_id,"Новая оплата #"+str(opa)+"\n\nСумма: "+str(a[2])+"₽"+"\nОплачено: qiwi\nКто оплатил: "+str(message.from_user.id)+"\nTelegram никнейм: @"+str(message.from_user.username)+"\nВремя: "+str(current_time))
                            sql = """
                            UPDATE nomeraoplati
                            SET num = ? 
                            WHERE num = ?
                            """
                            data = (opa, int(opa - 1))
                            c.execute(sql, data)
                            conn.commit()
                            aajajajajajjaj = 10
                try:
                    aajajajajajjaj
                except:
                    msg = bot.send_message(message.chat.id,'Оплата не найдена!',reply_markup=markupopl3)
                    bot.register_next_step_handler(msg, balance4)
        except:
            msg = bot.send_message(message.chat.id, 'Что-то пошло не так! Пожалуйста, попробуйте еще раз или в другое время', reply_markup=markupopl3)
            bot.register_next_step_handler(msg, balance4)

    else:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = (int(message.chat.id),)
        c.execute('SELECT * FROM payments WHERE id=?', t)
        a = c.fetchone()
        url = "https://qiwi.com/payment/form/99999?extra['account']=" + str(nickname) + "&extra['comment']=" + str(int(a[1])) + "&amountInteger=" + str(int(a[2])) + "&amountFraction=0&currency=643&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"
        msg = bot.send_message(message.chat.id, 'Обязательно укажите комментарий к платежу!\n\nВаш комментарий: ' + str(int(a[1])) + '\n\nСумма: ' + str(int(a[2])) + '\nНельзя менять никакие данные,иначе платеж не зачислится автоматически\n\nЕсли поле никнейма оказалось пустым, введите туда "BOOSTME" (без кавычек)\n\nОплатить баланс можно по ссылке ниже:\n' + str(url),reply_markup=markupopl3)
        bot.register_next_step_handler(msg, balance4)

@bot.message_handler(func=lambda message: message.text == "Репорт")
def report(message):
    if message.chat.id == group_id:
        bot.send_message(message.chat.id, 'Бот не работает в беседах')
    else:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = (int(message.chat.id),)
        c.execute('SELECT * FROM banlist WHERE id = ?',t)
        fo = c.fetchone()
        if not fo == None:
            bot.send_message(message.chat.id, "Вам заблокирована возможность писать репорты", reply_markup=markup)
        else:
            msg = bot.send_message(message.chat.id, "Введите сообщение для администрации:", reply_markup=markupnazad)
            bot.register_next_step_handler(msg, nnn)

def nnn(message):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reporti')
    a = c.fetchone()
    a = int(a[0])
    a = a + 1
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
    else:
        if len(str(message.text)) < 10:
            msg = bot.send_message(message.chat.id, "Репорт только от 10 символов!", reply_markup=markupnazad)
            bot.register_next_step_handler(msg, nnn)
        else:
            bot.send_message(message.chat.id, "Ваше сообщение отправлено", reply_markup=markup)
            bot.send_message(group_id, 'Новый репорт #'+str(a)+'\nКто написал: '+str(message.chat.id)+'\nТелеграмм никнейм: @'+str(message.from_user.username)+'\nТекст репорта: '+str(message.text))
            sql = """
            UPDATE reporti
            SET id = ? 
            WHERE id = ?
            """
            data = (a, int(a-1))
            c.execute(sql, data)
            conn.commit()

@bot.message_handler(commands=['admin'])
def admin(message):
    global markupadmin
    markupadmin = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рассылка")
    item2 = types.KeyboardButton("Купон")
    markupadmin.add(item1,item2,btn0)
    if message.chat.id == group_id:
        bot.send_message(message.chat.id, 'В беседах бот не работает')
    else:
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

def admin2(message):
    if message.text == "Рассылка":
        msg = bot.send_message(message.chat.id, 'Введите ваше сообщение:', reply_markup=markupnazad)
        bot.register_next_step_handler(msg, rassilka)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Добро пожаловать в главное меню! Выберите действие:", reply_markup=markup)
    elif message.text == "Купон":
        params = {'api_token':api_token}
        r = requests.get('https://vkmix.com/api/2/getBalance', params=params)
        n = r.json()
        msg = bot.send_message(message.chat.id, 'Текущий баланс: '+str(n['response']),reply_markup=markupkupon)
        bot.register_next_step_handler(msg, vvestik)

def vvestik(message):
    if message.text == 'Назад':
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
    if message.text == 'Назад':
        msg = bot.send_message(message.chat.id, 'Меню администратора', reply_markup=markupadmin)
        bot.register_next_step_handler(msg, admin2)
    else:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        m = c.fetchall()
        try:
            for i in range (len(m)):
                bot.send_message(m[i][0], message.text)
            msg = bot.send_message(message.chat.id, 'Рассылка успешно отправлена',reply_markup=markupadmin)
            bot.register_next_step_handler(msg, admin2)
        except:
            msg = bot.send_message(message.chat.id, 'Рассылка отправлена неуспешно!\nБот не нашел како-то чат!', reply_markup=markupadmin)
            bot.register_next_step_handler(msg, admin2)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def xz(message):
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
                    bot.send_message(group_id, 'Что-то пошло не так!')
        else:
            try:
                a = message.json['reply_to_message']['text']
                f = f = a.split('\n')
                f = f[1]
                f = f[12:]
                f = int(f)
                bot.send_message(f, 'Вам пришел ответ от администрации: ' + str(message.text))
                bot.send_message(message.chat.id, 'Ответ успешно отправлен')
            except:
                pass
    else:
        bot.send_message(message.chat.id, 'Такой команды не существует')

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
                for i in range(len(o)):
                    if int(o[i][2]) == 1:
                        bot.send_message(int(o[i][0]),'Предупреждение о низком балансе! Текущий баланс составляет: ' + str(a))
                time.sleep(300)
            else:
                time.sleep(300)
        except:
            time.sleep(300)
            continue

def tripler():
    while True:
        try:
            params = {'api_token': api_token}
            r = requests.get('https://vkmix.com/api/2/getTasks', params=params)
            a = r.json()['response']['items']
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute('SELECT * FROM zadania')
            e = c.fetchall()
            if a == []:
                time.sleep(300)
            else:
                for i in range((len(a))):
                    for b in range((len(e))):
                        if a[i] == None or e[b] == None:
                            continue
                        else:
                            if a[i]['network'] == e[b][1]:
                                if a[i]['section'] == e[b][2]:
                                    if a[i]['ordered_count'] == e[b][4]:
                                        if a[i]['status'] == 'success':
                                            bot.send_message(e[b][0],'Заказ успешно выполнен!')
                                            t = (int(e[b][6]),)
                                            c.execute("""DELETE from zadania where primirary_id = ?""", t)
                                            conn.commit()
                                            e[b] = None
                                            a[i] = None
                time.sleep(300)
        except:
            time.sleep(300)
            continue

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

if __name__ == '__main__':
    my_thread1 = threading.Thread(target=doubler)
    my_thread1.start()
    my_thread2 = threading.Thread(target=tripler)
    my_thread2.start()
    my_thread3 = threading.Thread(target=unban)
    my_thread3.start()
    bot.polling(none_stop=True)
