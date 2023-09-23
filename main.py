import telebot
from telebot import types
from telebot.types import Message
import random
from random import choice
import os
import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
from datetime import datetime


print("Бот запущен")
# start command

import sqlite3

bot = telebot.TeleBot('5957076810:AAEqRhV7wn4Wsv8hRUR3CMK9IvtCHx_YWLw')



import sqlite3  # Импортируйте библиотеку sqlite3

# ... Ваш код ...
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Вітаю {0.first_name}! \nЩоб почати тестування відправте команду /testlist'.format(
        message.from_user, bot.get_me()), parse_mode='html')

    # Проверьте, существует ли пользователь в базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Если пользователь не существует, выполните вставку в базу данных
        cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
        conn.commit()

    conn.close()

#wiki command
@bot.message_handler(commands=['wiki'])
def handle_wiki(message):
    # Получаем текст сообщения от пользователя
    user_input = message.text

    # Извлекаем ключевое слово
    keyword = user_input.split()[1]

    # Формируем запрос к API Википедии на україномовну версію
    url = f"https://uk.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles={keyword}"

    # Отправляем запрос и получаем ответ в формате JSON
    response = requests.get(url).json()\

    if "-1" in response["query"]["pages"]:
        bot.send_message(message.chat.id,f"Я не зміг знайти статтю по запиту {keyword}.\nСпробуйте змінити ключове слово або перевірити мову вводу.")
    else:
    # Извлекаем первый абзац текста и удаляем теги HTML
        page_id = list(response["query"]["pages"].keys())[0]
        text = response["query"]["pages"][page_id]["extract"]
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text().split("\n")[0]

    # Формируем сообщение для пользователя на украинском языке
        message_text = f"{text}\n\nПосилання на статтю: https://uk.wikipedia.org/wiki/{keyword}"

    # Отправляем сообщение пользователю
        bot.send_message(message.chat.id, message_text)

import sqlite3  # Добавьте этот импорт в начало вашего кода

@bot.message_handler(commands=['send'])
def send_start_handler(message):
    admins = [1899500715]  # список ID адміністраторів
    if message.from_user.id not in admins:
        bot.send_message(message.chat.id, 'Ви не отримали доступ для використання цієї команди.')
        return

    bot.send_message(message.chat.id, 'Надішліть повідомлення або фото з описом для розсилки.')

    # Встановлюємо стан очікування повідомлення для користувача
    bot.register_next_step_handler(message, send_message_to_users)

def send_message_to_users(message):
    # Отримуємо список користувачів з бази даних
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    joined_users = cursor.fetchall()
    conn.close()

    count = 0  # Лічильник відправлених повідомлень

    for user_id in joined_users:
        user_id = user_id[0]

        try:
            # Відправляємо повідомлення або фото з описом без видимості пересланого повідомлення
            if message.text:
                bot.send_message(user_id, message.text)
            elif message.photo:
                bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)

            count += 1  # Збільшуємо лічильник відправлених повідомлень
        except Exception as e:
            print(f"Помилка при відправці повідомлення користувачу {user_id}: {str(e)}")
            continue

    # Повідомляємо адміністратора, скільки користувачів отримали повідомлення
    bot.send_message(message.chat.id, f'Повідомлення відправлено {count} людям.')





    
@bot.message_handler(commands=['chat_commands'])
def start_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Вітаю {0.first_name}! \nСписок команд для спільного чату:\n1./cookies - дізнатися баланс печива (якщо відповісти на чиєсь повідомлення бот покаже баланс тої людини)\n2./karma - дізнатися рівень карми.Карму можна змінити написавши + чи - у відповідь на повідомленя (якщо відповісти на чиєсь повідомлення бот покаже баланс тої людини)\n3.Удача - випробуй свою удачу\n4.Відправити_печиво *число* - у відповідь на повідомлення ви можете відправити печиво іншому учаснику чату\n5.Топ_печиво - покаже топ 10 користувачів по кількості печива\n6.Топ_карма - покаже топ 10 користувачів по рівню карми\nВзаємодія - відправить кількість команд для взаємодії.'.format(
        message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['info'])
def start_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, "Я бот створений командою BioLogics для підготовки до тестів по різним дисциплінам.\nСписок команд:\n/testlist - обрати тест;\n/news - актуальні новини;\n/feedback - зворотній зв'язок\n/wiki + текст - бот знайде статтю у вікіпедії (приклад вводу команди /wikі біологія)\n/chat_commands - список команд для спільного чату\nПідписуйся на наш канал https://t.me/tavernofbiologics  ".format(
        message.from_user, bot.get_me()), parse_mode='html')

@bot.message_handler(commands=['developers'])
def start_message(message):
        time.sleep(2)
        bot.send_chat_action(message.chat.id, 'typing')

        bot.send_message(message.chat.id, 'Вітаю {0.first_name}! \nЗавдяки цим людям я можу вам допомогати:\n@Sarkitsyzm\n@Leshiy_v_lesy\n@avadfghj\n@denyskochenko\n@Aida_Lib\n@anastaciaturchin'.format(
        message.from_user, bot.get_me()), parse_mode='html')

@bot.message_handler(commands=['testlist'])
def test_handler(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,'Ось список тестів\n\nГістологія\n1./histologytest - тест на повторення препаратів з гістології.\n2./numbertest - дати назви позначенням на препараті.\n3./test1 - тест на 10 випадково обраних питань з гістології (назва препарату та позначення)\n4./zoologytest - тест з зоології безхребетних')
    if not str(message.chat.id) in JoinedUsers:
        JoinedFile = open("joined.txt","a")
        JoinedFile.write(str(message.chat.id) + "\n")
        JoinedUsers.add(message.chat.id)



@bot.message_handler(commands=['zoologytest'])
def zoo_test(message):
    zoobot = random.choice(zoobotes)
    answers = random.sample(zoobot['answers'], len(zoobot['answers']))
    keyboard11 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for answer in answers:
        keyboard11.add(telebot.types.KeyboardButton(answer))
    bot.send_message(message.chat.id, zoobot['text'], reply_markup=keyboard11)
    bot.register_next_step_handler(message, lambda m: check_answeres(m, zoobot))

def check_answeres(message, question):
    nexts1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnnext = telebot.types.KeyboardButton("Продовжити")
    nexts1.add(btnnext)

    if message.text == question['correct_ansed']:
        bot.reply_to(message, 'Це правильна відповідь', reply_markup=nexts1)
    else:
        nextqs = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnnexqt = telebot.types.KeyboardButton("Продовжити")
        nextqs.add(btnnext)
        bot.reply_to(message, f'Неправильно. Правильна відповідь: {question["correct_ansed"]}', reply_markup=nextqs)

@bot.message_handler(commands=['histologytest'])
def histology_test_handler(message):
    question = random.choice(questionds1)
    photo = question['photo']
    answers = random.sample(question['answers'], len(question['answers']))
    keyboard1 = telebot.types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True)
    for answer in answers:
        keyboard1.add(telebot.types.KeyboardButton(answer))
    bot.send_photo(message.chat.id, photo,
                   caption=question['text'], reply_markup=keyboard1)
    bot.register_next_step_handler(
        message, lambda m: check_answersq(m, question))



def check_answersq(message, question):

    nexts2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnnext2 = telebot.types.KeyboardButton("Далі")
    nexts2.add(btnnext2)
    if message.text == question['correct_ansed']:
        bot.reply_to(message, 'Ваша відповідь правильна ', reply_markup=nexts2)
    else:
        bot.reply_to(
            message, f'Неправильно. Ось правильна відповідь: {question["correct_ansed"]}', reply_markup=nexts2)


@bot.message_handler(commands=['numbertest'])
def test_handler(message):
    gistobot = random.choice(gistoquest)
    photo = gistobot['photo']
    answers = random.sample(gistobot['answers'], len(gistobot['answers']))
    keyboard1 = telebot.types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True)
    for answer in answers:
        keyboard1.add(telebot.types.KeyboardButton(answer))
    bot.send_photo(message.chat.id, photo,
                   caption=gistobot['text'], reply_markup=keyboard1)
    bot.register_next_step_handler(
        message, lambda m: check_answers(m, gistobot))

def check_answers(message, question):
    nexts1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnnext = telebot.types.KeyboardButton("Наступне питання")
    nexts1.add(btnnext)

    if message.text == question['correct_answer']:
        bot.reply_to(message, 'Це правильна відповідь', reply_markup=nexts1)
    else:
        nexts = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnnext = telebot.types.KeyboardButton("Наступне питання")
        nexts.add(btnnext)
        bot.reply_to(
            message, f'Неправильно. Правильна відповідь: {question["correct_answer"]}', reply_markup=nexts)



def check_answeres(message, question):
    nexts1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnnext = telebot.types.KeyboardButton("Продовжити")
    nexts1.add(btnnext)

    if message.text == question['correct_ansed']:
        bot.reply_to(message, 'Це правильна відповідь', reply_markup=nexts1)
    else:
        nextqs = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnnexqt = telebot.types.KeyboardButton("Продовжити")
        nextqs.add(btnnext)
        bot.reply_to(message, f'Неправильно. Правильна відповідь: {question["correct_ansed"]}', reply_markup=nextqs)

@bot.message_handler(commands=['test1'])
def test_handlerу(message):
    chosen_questions = random.sample(foourtest, 10)  # выбираем случайным образом 2 вопроса из списка
    user_answers = []
    current_question = 0

    def send_question():
        nonlocal current_question
        foourtest = chosen_questions[current_question]
        photo = foourtest['photo']
        answers = random.sample(foourtest['answers'], len(foourtest['answers']))
        keyboardg = telebot.types.ReplyKeyboardMarkup(
            row_width=1, resize_keyboard=True)
        for answer in answers:
            keyboardg.add(telebot.types.KeyboardButton(answer))
        bot.send_photo(message.chat.id, photo,
                       caption=foourtest['text'], reply_markup=keyboardg)
        bot.register_next_step_handler(
            message, lambda m, q=foourtest: check_answer(m, q, user_answers))

    def check_answer(message, foourtest, user_answers):
        user_answer = message.text
        user_answers.append(user_answer)

        nonlocal current_question
        current_question += 1

        if current_question < len(chosen_questions):
            send_question()
        else:
            markupg = telebot.types.ReplyKeyboardRemove(message.chat.id)
            # show final results
            results = []
            for i, foourtest in enumerate(chosen_questions):
                results.append(f"Питання №{i+1}. {foourtest['text']} \nВаша відповідь: {user_answers[i]}, \nПравильна відповідь: {foourtest['correct_ans']}")
            num_correct = sum([1 for i in range(10) if user_answers[i] == chosen_questions[i]['correct_ans']])
            results.append(f"Кількість правильних відповідей: {num_correct}/10")
            bot.send_message(message.chat.id, "\n\n".join(results))

    send_question()
#bd база данных и ответы бота
#karma
@bot.message_handler(commands=['karma'])
def showkarma(message):
    replieduser = None
    repliedusername = None

    # проверяем, есть ли ответ на сообщение
    if message.reply_to_message:
        replieduser = message.reply_to_message.from_user.id
        repliedusername = message.reply_to_message.from_user.first_name
    else:
        replieduser = message.from_user.id
        repliedusername = message.from_user.first_name

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # создаем таблицу, если она еще не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER,points INTEGER,users INTEGER)")

    # получаем значение кармы для пользователя
    result = cursor.execute("SELECT karma FROM users WHERE id=? AND username=?", (replieduser, repliedusername)).fetchone()
    if result:
        karma = result[0]
        bot.send_message(message.chat.id, f'Карма користувача {repliedusername}: {karma}✨.')
    else:
        bot.send_message(message.chat.id, f'У користувача {repliedusername} карма дорівнює 0.Дайте відповідь "+" на одне з його повідомлень щоб збільшити його карму,а також "-" щоб зменшити.')

    cursor.close()
    conn.close()

# Імпорт бібліотеки sqlite3 та datetime
import sqlite3
from datetime import datetime, timedelta

# luck
@bot.message_handler(func=lambda message: 'удача' in message.text.lower())
def luck(message):
    # Отримати інформацію про користувача
    userid = message.from_user.id
    username = message.from_user.first_name
    
    # Підключення до бази даних та створення таблиці, якщо потрібно
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL)")
        
        # Перевірка, чи існує користувач в базі даних
        result = cursor.execute("SELECT * FROM users WHERE id=?", (userid,)).fetchone()
        if result is None:
            # Якщо користувача немає в базі даних, то вставте новий рядок
            cursor.execute("INSERT INTO users (id, username, karma, points, users, last_command_time) VALUES (?, ?, ?, ?, ?, ?)", (userid, username, 0, 0, 0, datetime.now()))
        else:
            # Якщо користувач існує, оновіть час останньої команди
            cursor.execute("UPDATE users SET last_command_time=? WHERE id=?", (datetime.now(), userid))

        # Перевірка, чи може користувач використовувати команду (один раз на годину)
        if result and result[5]:
            last_command_time = datetime.strptime(result[5], '%Y-%m-%d %H:%M:%S.%f')
        else:
            last_command_time = None
        time_since_last_command = datetime.now() - last_command_time if last_command_time else timedelta(seconds=3600)
        if time_since_last_command.total_seconds() < 3600:
            remaining_time = int(3600 - time_since_last_command.total_seconds())
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            bot.send_message(message.chat.id, f"Ай-яй, команду можна використати лише один раз на годину. Чекай ще {minutes} хвилин {seconds} секунд.")
            return

        # Генерування випадкових очок та карми з ймовірністю 20% негативних значень
        points = random.randint(1, 100)
        karma = random.randint(1, 10)
        if random.random() < 0.2:
            points = -points
        if random.random() < 0.2:
            karma = -karma

        # Оновлення бази даних новими значеннями та поточним часом
        cursor.execute("UPDATE users SET points=points+?, karma=karma+?, last_command_time=? WHERE id=?", (points, karma, datetime.now(), userid))
        conn.commit()

        # Складання та надсилання повідомлення з результатами
        points_str = f"{points:+d}" if points >= 0 else f"{points:d}"
        karma_str = f"{karma:+d}" if karma >= 0 else f"{karma:d}"
        bot.send_message(message.chat.id, f"Вирішив випробувати свою удачу?\nОсь результат:\n{karma_str}✨\n{points_str}🍪")



#give cookies admin
adminsid = ['1899500715', '5838139796','1686685747']
admins = ['1899500715', '5838139796','1686685747']
import datetime
from datetime import datetime
@bot.message_handler(func=lambda message: 'дар_печиво' in message.text.lower())
def give_points(message):
    # Перевірка, чи є повідомлення відповіддю на інше повідомлення
    if message.reply_to_message is None:
        bot.send_message(message.chat.id, 'Ця команда може бути виконана тільки відповіддю на повідомлення')
        return

    replied_user = message.reply_to_message.from_user
    user_id = replied_user.id
    user_name = replied_user.first_name
    user_username = replied_user.username

    if str(replied_user.id) in admins:
        bot.send_message(message.chat.id, 'Ви не можете відправити печиво собі,адміну чи боту.')
        return

    # Перевірка, чи є користувач адміністратором
    if str(message.from_user.id) not in adminsid:
        bot.send_message(message.chat.id, 'У вас недостатньо прав на виконання цієї команди')
        return

    # Отримання суми для дарування
    match = re.search(r'дар_печиво\s+(\d+)', message.text.lower())
    if not match:
        bot.send_message(message.chat.id, 'Ви маєте вказати суму яку хочете подарувати.\nПриклад повідомлення "Дар_печиво 10"')
        return
    amount = int(match.group(1))

    # Оновлення балансу користувача
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_karma_time INTEGER,last_reply_time INTEGER)")
        result = cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (user_id, user_name)).fetchone()
        if result:
            points = (result[0] or 0) + amount
            cursor.execute("UPDATE users SET points=points + ?, last_command_time=? WHERE id=? AND username=?", (amount, datetime.now(), user_id, user_name))

        # Сохранение изменений в базе данных
            conn.commit()
            Иbot.send_message(message.chat.id, f'@{user_username} сподобався аміністратору бота і отримав {amount}🍪.')


#send cookies
@bot.message_handler(func=lambda message: 'відправити_печиво' in message.text.lower())
def send_points(message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, 'Оберіть кому хочете відправити печиво')
        return

    replieduser = message.reply_to_message.from_user.id
    repliedname = message.reply_to_message.from_user.first_name
    repliedusername = message.reply_to_message.from_user.username
    userid = message.from_user.id
    username = message.from_user.first_name
    if replieduser == userid:
        bot.send_message(message.chat.id, 'Ви не можете відправити печиво собі.')
        return
    # Получаем сумму, которую нужно отправить, из сообщения пользователя
    match = re.search(r'відправити_печиво\s+(\d+)', message.text.lower())
    if not match:
        bot.send_message(message.chat.id, 'Ви маєте вказати суму яку хочете відправити.\nПриклад повідомлення "Відправити_печиво 10"')
        return
    amount = int(match.group(1))

    # Проверяем, достаточно ли у пользователя points для отправки указанной суммы
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_karma_time INTEGER,last_reply_time INTEGER)")
        result = cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (userid, username)).fetchone()
        if result is None or result[0] < amount:

            bot.send_message(message.chat.id, 'У вас недостатньо печива.')
            return
        points = result[0]

        # Вычитаем сумму из points пользователя и начисляем ее пользователю, которому ответили на сообщение
        points -= amount
        cursor.execute("UPDATE users SET points=?, last_command_time=? WHERE id=? AND username=?", (points, datetime.now(), userid, username))
        result = cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (replieduser, repliedname)).fetchone()
        if result:
            replied_points = (result[0] or 0) + amount
            cursor.execute("UPDATE users SET points=?, last_command_time=? WHERE id=? AND username=?", (replied_points, datetime.now(), replieduser, repliedname))
            conn.commit()
        else:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (userid, username, 0, 0, 0, 0, 0, 0))
            conn.commit()
        bot.send_message(message.chat.id, f'Ви відправили {amount}🍪 {repliedname}.\nВаш баланс:{points}🍪')

#cookies
@bot.message_handler(commands=['cookies'])
def pointsmessage(message):
    if message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
    else:
        username = message.from_user.first_name

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP)")
    cursor.execute("SELECT points FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    if result:
        points = result[0]
        bot.send_message(message.chat.id, f'Кількість 🍪 {username}: {points}')
    else:
        cursor.execute("INSERT INTO users (username, karma, points) VALUES (?, 0, 0)", (username,))
        conn.commit()
        bot.send_message(message.chat.id, f'{username} ще не має 🍪')
    conn.close()

storage = dict()

def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)

def set_data_storage(user_id, key, value):
    storage[user_id][key] = value

def get_data_storage(user_id):
    return storage[user_id]



@bot.message_handler(func=lambda message: 'обійняти' in message.text.lower())
def hug(message):

    if not message.reply_to_message:
        bot.send_message(message.chat.id, 'Оберіть користувача якого хочете обійняти.')
        return
    replieduser = message.reply_to_message.from_user.id
    repliedname = message.reply_to_message.from_user.first_name
    repliedusername = message.reply_to_message.from_user.username
    userid = message.from_user.id
    username = message.from_user.first_name
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP)")
        result = cursor.execute("SELECT * FROM users WHERE id=? AND username=?", (userid, username)).fetchone()
        if not result:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?,?)", (userid, username, 0, 0, 0, 0, 0,0))
            conn.commit()



    if replieduser == userid:
        bot.send_message(message.chat.id, 'Ви не можете обійняти себе.')
        return


    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
       
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER,points INTEGER,users INTEGER)")
        result = cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (userid, username)).fetchone()
        if result:
            points = result[0]
            random_number = random.randint(1, 100)

            if random_number <= 0.2 * 100:
                points -= random_number
                bot.send_message(message.chat.id, f"{repliedname} відмовився обійматися, тому {username} втратив {random_number}🍪.")
            elif random_number <= 0.8 * 100:
                points += random_number
                bot.send_message(message.chat.id, f"{username} обійняв {repliedname} і отримав {random_number}🍪.")
            cursor.execute("UPDATE users SET points=? WHERE id=? AND username=?", (points, userid, username))
            conn.commit()





#coffee
@bot.message_handler(func=lambda message: 'запросити_на_каву' in message.text.lower())
def hug(message):

    if not message.reply_to_message:
        bot.send_message(message.chat.id, 'Оберіть користувача якого хочете запросити на каву.')
        return
    replieduser = message.reply_to_message.from_user.id
    repliedname = message.reply_to_message.from_user.first_name
    repliedusername = message.reply_to_message.from_user.username
    userid = message.from_user.id
    username = message.from_user.first_name
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP)")
        result = cursor.execute("SELECT * FROM users WHERE id=? AND username=?", (userid, username)).fetchone()
        if not result:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?,?)", (userid, username, 0, 0, 0, 0, 0,0))
            conn.commit()



    if replieduser == userid:
        bot.send_message(message.chat.id, 'Ви не можете запросити себе.')
        return


    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
       
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER,points INTEGER,users INTEGER)")
        result = cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (userid, username)).fetchone()
        if result:
            points = result[0]
            random_number = random.randint(1, 100)

            if random_number <= 0.2 * 100:
                points -= random_number
                bot.send_message(message.chat.id, f"{repliedname} відмовився пити каву, тому {username} втратив {random_number}🍪.")
            elif random_number <= 0.8 * 100:
                points += random_number
                bot.send_message(message.chat.id, f"{username} випив кави з {repliedname} і отримав {random_number}🍪.")
            cursor.execute("UPDATE users SET points=? WHERE id=? AND username=?", (points, userid, username))
            conn.commit()

#pin message
@bot.message_handler(
    content_types=['pinned_message'])  # Хендлер описывающий поведение бота после того, как было закрепленно сообщение
def pinned_msg(message):  # Запуско основной функции хендлера
    try:  # Пытаемся выполнить команду приведеную ниже
        bot.send_chat_action(message.chat.id, 'typing');
        time.sleep(1)
        msg12 = random.choice(msgpin)
        bot.reply_to(message, text = msg12
                     , disable_notification=True)   # Отвечаем на закрепленное сообщение
    except OSError:  # Игнорируем ошибку по таймауту, если телеграмм успел разорвать соединение сс времени прошлой сесии
        print("PinnedError - Sending again after 3 seconds!!!")  # Выводим ошибку в консоль
        time.sleep(3)  # Делаем паузу в 3 секунды и выполняем команду приведеную ниже
        bot.reply_to(message, text='Ну, теперь заживем',
                     disable_notification=True)
#vc message
@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    chance = random.randint(1, 100)
    if chance <= 6:
        bot.send_photo(message.chat.id, random.choice(photos))
    elif chance <= 16:
        messages = ['Ще одне голосове...', 'А тебе можна послухати', 'Я не хочу слухати голосові повідомлення', 'Відійшов на хвилинку,а тут купа голосових', 'У давнину гінця вішали, якщо він приносив голосове повідомлення','Твої голосові я послухаю','Шкода, що мені не додали функцію розпізнавання голосових...','У відповідь на голосове повідомлення я зазвичай кидаю відео, де я повільно пишу відповідь у блокноті.','Я більше не можу слухати голосові','Користувач встановив обмеження на отримання голосових повідомлень.']
        bot.reply_to(message, random.choice(messages))
    elif chance ==  100:
        random_texts = ["У тебе дуже гарний голос", "Ще б я знав навіщо ти це все говориш", "Мені тебе шкода"]
        random_text = random.choice(random_texts)
        pointed = random.randint(200, 500)
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET points=points+? WHERE id=? AND username=?", (pointed, message.from_user.id, message.from_user.first_name))
            conn.commit()
            cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (message.from_user.id, message.from_user.first_name))
            points = cursor.fetchone()[0]
        bot.reply_to(message, f"{random_text}, тримай печиво {pointed}🍪\nВаш баланс: {points}🍪")
    elif chance == 99:
        random_texetR = ["Мені не подобається твоя історія", "Я не хочу витрачати час на голосові повідомлення", "А чо, ти вмієш розказувати історії 😁","Мені набридло вас слухати","Господи... Це крінж!"]
        random_texet = random.choice(random_texetR)
        pointed = random.randint(100, 300)
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET points=points-? WHERE id=? AND username=?", (pointed, message.from_user.id, message.from_user.first_name))
            conn.commit()
            cursor.execute("SELECT points FROM users WHERE id=? AND username=?", (message.from_user.id, message.from_user.first_name))
            points = cursor.fetchone()[0]
        bot.reply_to(message, f"{random_texet} тому я забираю в тебе  {pointed}🍪\nВаш баланс: {points}🍪")

#new
@bot.message_handler(
    content_types=['new_chat_members'])  # Хендлер описывающий поведение бота при добавлении нового пользователя
def greeting(message):  # Запуско основной функции хендлера
 # Выводим в консоль имя нового пользователя
    try:  # Пытаемся выполнить команду приведеную ниже
        bot.send_chat_action(message.chat.id, 'typing');
        time.sleep(1)
        bot.reply_to(message, text='Вітаю у нашому чаті! '
                     , disable_notification=True)  # Выводим приветствие в чат
    except OSError:  # Игнорируем ошибку по таймауту, если телеграмм успел разорвать соединение сс времени прошлой сесии
        print("GreetingError - Sending again after 5 seconds!!!")  # Выводим ошибку в консоль
        time.sleep(3)  # Делаем паузу в 3 секунды и выполняем команду приведеную ниже
        bot.reply_to(message, text='Вітаю у нашому чаті!'
                     , disable_notification=True)  # Выводим приветствие в чат

#left
@bot.message_handler(
    content_types=['left_chat_member'])  # Хендлер описывающий поведение бота при выходе пользователя из чата
def not_greeting(message):  # Запуско основной функции хендлера# Выводим в консоль имя ушедшего пользователя
    try:  # Пытаемся выполнить команду приведеную ниже
        bot.send_chat_action(message.chat.id, 'typing');
        time.sleep(1)
        bot.reply_to(message, text='Шкода, що ви покинули наш чат...',
                     disable_notification=True)  # Выводим прощание в чат
    except OSError:  # Игнорируем ошибку по таймауту, если телеграмм успел разорвать соединение сс времени прошлой сесии
        print("LeftError - Sending again after 5 seconds!!!")  # Выводим ошибку в консоль
        time.sleep(3)  # Делаем паузу в 3 секунды и выполняем команду приведеную ниже
        bot.reply_to(message, text='Шкода, що ви покинули наш чат...',
                     disable_notification=True)  # Выводим прощание в чат




def get_last_command_time(user_id):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS commands (user_id INTEGER, time INTEGER)")
        result = cursor.execute("SELECT time FROM commands WHERE user_id=?", (user_id,)).fetchone()
        if result:
            return result[0]
        else:
            return 0

import requests
import datetime
import calendar
import locale

api_key = '0ed7b037d48833177bc09fcb9bc23bc1'
lang = 'uk'

@bot.message_handler(commands=['weather_week'])
def send_weather_week(message):
    # Задаємо локаль
    locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
    city = message.text.replace('/weather_week', '').strip()
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&lang={lang}'
    response = requests.get(url)
    data = response.json()
    if 'list' in data:
        # Створюємо словник, де ключ - це день тижня, а значення - рядок з даними про погоду на цей день
        weather_by_day = {}
        for forecast in data['list']:
            # Ізвлечення дати та часу з даних прогнозу
            timestamp = forecast['dt']
            date = datetime.fromtimestamp(timestamp)
            # Перевіряємо, що час прогнозу дорівнює 12:00
            if date.time().hour == 12:
                # Перетворення часової мітки в рядок дати з українськими назвами днів тижня
                day = date.strftime('%A').capitalize()
                # Ізвлечення даних про погоду
                weather = forecast['weather'][0]['description']
                temperature = forecast['main']['temp']
                temperature_in_celsius = round(temperature - 273.15, 2)
                # Формирование строки с данными о погоде на день
                response_text = f"{weather}, {temperature_in_celsius} °C"
                # Добавляем строку с данными о погоде в словарь
                if day not in weather_by_day:
                    weather_by_day[day] = response_text
                else:
                    weather_by_day[day] += '\n' + response_text
        # Создаем строку для отправки сообщения
        response_text = f"Прогноз погоди для міста {city}:\n\n"
        for day, weather_data in weather_by_day.items():
            response_text += f"{day}:\n{weather_data}\n\n"
        # Отправляем сообщение с данными о погоде на неделю
        bot.reply_to(message, response_text)
    else:
        # Если данных о прогнозе нет, отправляем сообщение об ошибке
        bot.reply_to(message, "Данні для цього міста відсутні.")


#+-
@bot.message_handler(func=lambda message: message.text in ['+', '-'])
def addkarma(message):
    replieduser = message.reply_to_message.from_user.id
    repliedusername = message.reply_to_message.from_user.first_name
    userid = message.from_user.id
    username = message.from_user.first_name
    current_time = int(time.time())

    if replieduser == userid:
        bot.send_message(message.chat.id, 'Ви не можете змінити свою карму.')
        return

    last_command_time = get_last_command_time(userid)
    if current_time - last_command_time < 3600:
        remaining_time = 3600 - (current_time - last_command_time)
        bot.send_message(message.chat.id, f"Цьому користувачу нещодавно вже змінили карму,чекай ще {remaining_time // 60} хвилин і {remaining_time % 60} секунд.")
        return

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_cof_time TIMESTAMP DEFAULT NULL, last_biy TIMESTAMP DEFAULT NULL, last_karma_time INTEGER, last_reply_time INTEGER, kunica_name TEXT, ferret_level INTEGER, photo TEXT, work_type INTEGER DEFAULT 0, work_time TIMESTAMP DEFAULT '1990-01-01 00:00:00',last_work_stop INTEGER DEFAULT 0  )")
        result = cursor.execute("SELECT karma, last_karma_time, last_reply_time FROM users WHERE id=? AND username=?", (replieduser, repliedusername)).fetchone()
        if result:
            karma = result[0]
            last_karma_time = result[1]
            last_reply_time = result[2]
            if last_karma_time is None:
                last_karma_time = current_time
            else:
                try:
                    last_karma_time = int(last_karma_time)
                except ValueError:
                    last_karma_time = None
            time_diff = current_time - last_karma_time if last_karma_time is not None else 3600
            if time_diff < 3600:
                remaining_time = 3600 - time_diff
                bot.send_message(message.chat.id, f"Цьому користувачу нещодавно вже змінили карму,чекай ще {remaining_time // 60} хвилин {remaining_time % 60} секунд.")
                return
            if message.text == '+':
                karma += 1
                messagetext = f'Карма користувача {repliedusername} збільшилась до {karma}✨.'
            else:
                karma -= 1
                messagetext = f'Карма користувача {repliedusername} зменшилась до {karma}✨.'
            cursor.execute("UPDATE users SET karma=?, last_karma_time=?, last_reply_time=? WHERE id=? AND username=?", (karma, current_time, current_time, replieduser, repliedusername))

            conn.commit()
            bot.send_message(message.chat.id, messagetext)

            # записываем время отправки сообщения с изменением кармы в таблицу пользователя
            cursor.execute("UPDATE users SET last_karma_time=? WHERE id=? AND username=?", (current_time, replieduser, repliedusername))
            conn.commit()

        else:
            if message.text == '-':
                karma = -1
                messagetext = f'Карма користувача  {repliedusername} зменшилась до {karma}✨.'
            else:
                karma = 1
                messagetext = f'Карма користувача {repliedusername} збільшилась до {karma}✨.'
            cursor.execute("INSERT INTO users (id, username, karma, last_karma_time, last_reply_time) VALUES (?, ?, ?, ?, ?)", (replieduser, repliedusername, karma, current_time, current_time))
            conn.commit()
            bot.send_message(message.chat.id, messagetext)

#куниця 
def get_random_photo():

    photos = ['куниця (1).jpg', 'куниця (2).jpg', 'куниця (3).jpg', 'куниця (4).jpg', 'куниця (5).jpg', 'куниця (6).jpg', 'куниця (7).jpg', 'куниця (8).jpg', 'куниця (9).jpg', 'куниця (10).jpg', 'куниця (11).jpg', 'куниця (12).jpg', 'куниця (13).jpg', 'куниця (14).jpg', 'куниця (15).jpg', 'куниця (16).jpg', 'куниця (17).jpg', 'куниця (18).jpg', 'куниця (19).jpg', 'куниця (20).jpg', 'куниця (21).jpg', 'куниця (22).jpg', 'куниця (23).jpg', 'куниця (24).jpg', 'куниця (25).jpg', 'куниця (26).jpg', 'куниця (27).jpg', 'куниця (28).jpg']  # список фото
    return random.choice(photos)

# функция для сохранения фото и имени в базу данных
def save_photo_to_db(user_id, username, photo):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_karma_time INTEGER,last_reply_time INTEGER,kunica_name TEXT, photo TEXT)")
        cursor.execute("SELECT kunica_name FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        if result:
            old_username = result[0]
            if old_username != username:
                cursor.execute("UPDATE users SET kunica_name=? WHERE id=?", (username, user_id))
                conn.commit()
                return True
            else:
                return False
        else:
            cursor.execute("INSERT INTO users (id, kunica_name, photo) VALUES (?, ?, ?)", (user_id, username, photo))
            conn.commit()
            return True


# by pet
@bot.message_handler(func=lambda message: 'купити_куницю' in message.text.lower())
def add_kunica_photo(message):
    user_id = message.from_user.id
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_cof_time TIMESTAMP DEFAULT NULL, last_biy TIMESTAMP DEFAULT NULL, last_karma_time INTEGER, last_reply_time INTEGER, kunica_name TEXT, ferret_level INTEGER, photo TEXT, work_type INTEGER DEFAULT 0, work_time TIMESTAMP DEFAULT '1990-01-01 00:00:00',last_work_stop INTEGER DEFAULT 0  )")

        cursor.execute("SELECT photo, kunica_name, points FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        if result:
            photo, kunica_name, points = result
            if photo and kunica_name:
                bot.send_message(message.chat.id, "В тебе вже є куниця")
            else:
                if points is None:
                    points = 0
                if points >= 5000:
                    photo = get_random_photo()
                    kunica_name = random.choice(['Куница', 'Пушок', 'Лисичка','Арчі','Белла','Клео','Сімба','Тедді','Вінні','Ванда','Ассоль','Аліса','Сніжинка','Джессі','Ожина','Зефірка','Лаккі'])
                    saved = save_photo_to_db(user_id, kunica_name, photo)
                    if saved:
                        with open(photo, 'rb') as photo_file:
                            bot.send_photo(message.chat.id, photo_file, caption=f"Вітаю! Твою куницю звати {kunica_name}.Щоб змінити ім'я напиши 'назвати_куницю + нове ім'я' ")
                        cursor.execute("UPDATE users SET kunica_name=?, photo=?, points=points-5000 WHERE id=?", (kunica_name, photo, user_id))
                        conn.commit()
                else:
                    bot.send_message(message.chat.id, f"У тебе недостатньо печива щоб купити куницю,потрібно 5000🍪,а у тебе {points}🍪")
        else:
            cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
            conn.commit()
            bot.send_message(message.chat.id, "Спробуй купити куницю ще раз")
#pet prof
@bot.message_handler(func=lambda message: 'моя_куниця' in message.text.lower())
def view_kunica_profile(message):
    user_id = message.from_user.id
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_karma_time INTEGER,last_reply_time INTEGER,kunica_name TEXT, photo TEXT)")
        cursor.execute("SELECT photo, kunica_name, ferret_level FROM users WHERE id=? AND photo IS NOT NULL AND kunica_name IS NOT NULL", (user_id,))
        result = cursor.fetchone()
        if result is not None:
            photo, kunica_name, ferret_level = result
            
            # Проверяем, если ferret_level равно None, устанавливаем значение по умолчанию 0
            if ferret_level is None:
                ferret_level = 0
            
            if 0 <= ferret_level <= 10:
                level_text = "Рівень куниці: 0"
            elif 11 <= ferret_level <= 50:
                level_text = "Рівень куниці: 1"
            elif 51 <= ferret_level <= 100:
                level_text = "Рівень куниці: 2"
            else:
                level_text = "Некоректне значення рівня куниці"
            
            caption = f"Ім'я куниці: {kunica_name}\n{level_text}"
            bot.send_photo(message.chat.id, open(photo, 'rb'), caption=caption)
        else:
            bot.send_message(message.chat.id, 'У тебе ще немає куниці, напиши "купити_куницю" 🦊')



@bot.message_handler(func=lambda message: 'назвати_куницю' in message.text.lower())
def change_kunica_name(message):
    user_id = message.from_user.id
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, kunica_name TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP, photo TEXT)")
        cursor.execute("SELECT kunica_name, points FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        if result:
            old_kunica_name, user_points = result[0], result[1]
            try:
                new_kunica_name = message.text.split()[1]
                if user_points >= 2000:
                    saved = save_photo_to_db(user_id, new_kunica_name, None)
                    if saved:
                        cursor.execute("UPDATE users SET kunica_name=?, points=? WHERE id=?", (new_kunica_name, user_points - 2000, user_id))
                        conn.commit()
                        bot.send_message(message.chat.id, f"Чудово! ти назвав куницю {new_kunica_name} 🦊")
                    else:
                        bot.send_message(message.chat.id, f"Ти вже дав ім'я {new_kunica_name} своїй куниці")
                else:
                    bot.send_message(message.chat.id, f"У тебе недостатньо печива 🍪 щоб змінити ім'я куниці,Потрібно 2000🍪,а у тебе {user_points} 🍪")
            except IndexError:
                bot.send_message(message.chat.id, "Оберіть ім'я для куниці")
        else:
            bot.send_message(message.chat.id, 'У тебе ще немає куниці,напиши "купити_куницю" 🦊')


#command weather
API_KEY = '0ed7b037d48833177bc09fcb9bc23bc1'

# мова для перекладу
LANG = 'uk'



# обробник повідомлень
@bot.message_handler(commands=['weather'])
def send_weather(message):
    # отримання назви міста з повідомлення користувача
    city = message.text.replace('/weather', '').strip()

    # створення URL-адреси запиту до API openweathermap.org
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang={LANG}'

    # виконання запиту до API та отримання даних в форматі JSON
    response = requests.get(url)
    data = response.json()

    # перевірка наявності ключа 'weather' у відповіді JSON
    if 'weather' in data:
        # отримання даних про погоду з відповіді JSON, якщо вони доступні
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        # переведення температури з Кельвіна на Цельсій
        temperature_in_celsius = round(temperature - 273.15, 2)
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        # формування відповіді
        response_text = f"Погода в місті {city}: {weather}\n"
        response_text += f"Температура: {temperature_in_celsius} °C\n"
        response_text += f"Вологість: {humidity}%\n"
        response_text += f"Швидкість вітру: {wind_speed} м/с"
        # надіслання відповіді користувачу
        bot.reply_to(message, response_text)


@bot.message_handler(commands=['level'])
def get_ferret_level(message):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_cof_time TIMESTAMP DEFAULT NULL, last_biy TIMESTAMP DEFAULT NULL, last_karma_time INTEGER, last_reply_time INTEGER, kunica_name TEXT, ferret_level INTEGER, photo TEXT, work_type INTEGER DEFAULT 0, work_time TIMESTAMP DEFAULT '1990-01-01 00:00:00', last_work_stop INTEGER DEFAULT 0)")

    # Получаем значение колонки ferret_level для пользователя
    cursor.execute("SELECT ferret_level FROM users WHERE id=?", (message.from_user.id,))
    result = cursor.fetchone()
    
    # Задаем значение по умолчанию для level_text
    if result is not None:
        ferret_level = result[0]  # Присвоение полученного значения из базы данных переменной ferret_level
        if 0 <= ferret_level <= 10:
            level_text = "Рівень куниці: 0"
        elif 11 <= ferret_level <= 50:
            level_text = "Рівень куниці: 1"
        elif 51 <= ferret_level <= 100:
            level_text = "Рівень куниці: 2"
        elif 101 <= ferret_level <= 200:
            level_text = "Рівень куниці: 3"
        elif 201 <= ferret_level <= 300:
            level_text = "Рівень куниці: 4"
    else:
        level_text = "Рівень куниці: Не встановлено"

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()
    
    # Отправляем сообщение с уровнем куницы
    bot.reply_to(message, level_text)


from datetime import datetime, timedelta
@bot.message_handler(func=lambda message: 'гратися' in message.text.lower())
def play_with_ferret(message):
    user_id = message.from_user.id
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL,last_biy TIMESTAMP DEFAULT NULL,last_karma_time INTEGER, last_reply_time INTEGER, kunica_name TEXT,last_cof_time INTEGER,ferret_level INTEGER, photo TEXT)")

        # Получаем информацию о пользователе из базы данных
        cursor.execute("SELECT photo, ferret_level, last_cof_time FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()

        if result:
            photo, ferret_level, last_cof_time = result[0], result[1], result[2]
            if not photo:
                bot.send_message(message.chat.id, 'У тебе ще немає куниці,напиши "купити_куницю" 🦊')
            else:
                # Проверяем, прошло ли уже 30 минут с последнего использования команды
                if last_cof_time:
                    time_since_last_cof = datetime.now() - datetime.fromisoformat(last_cof_time)
                    if time_since_last_cof < timedelta(minutes=30):
                        remaining_time = timedelta(minutes=30) - time_since_last_cof
                        bot.send_message(message.chat.id, f"Ви можете грати з куницею лише раз на 30 хвилин. Залишилось {remaining_time.seconds // 60} хвилин {remaining_time.seconds % 60} секунд.")
                        return
                if ferret_level is None:
                    # Если ferret_level равен None, устанавливаем начальное значение
                    ferret_level = 0

                play_chance = random.randint(1, 100)
                if play_chance <= 35:
                    points = random.randint(1, 30)
                    ferret_level_increase = random.randint(1, 3)
                    new_ferret_level = ferret_level + ferret_level_increase
                    # Оновлюємо рівень куниці та поінти в базі даних
                    cursor.execute("UPDATE users SET ferret_level=?, points=points+? WHERE id=?", (new_ferret_level, points, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Ви успішно пограли з куницею! Ви отримуєте {points}🍪, і рівень вашої куниці підвищується на {ferret_level_increase}.")
                elif play_chance <= 55:
                    level_increase = random.randint(1, 5)
                    new_ferret_level = ferret_level + level_increase
                    # Оновлюємо рівень куниці в базі даних
                    cursor.execute("UPDATE users SET ferret_level=? WHERE id=?", (new_ferret_level, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Куниця відмовилась грати і пішла спати. Поточний рівень куниці підвищується на {level_increase}.")
                elif play_chance <= 60:
                    points_lost = random.randint(100, 400)
                    # Оновлюємо поінти в базі даних
                    cursor.execute("UPDATE users SET points=points-? WHERE id=?", (points_lost, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Куниця вас вкусила! Ви втрачаєте {points_lost}🍪.")
                elif play_chance <= 70:
                    bird_level_increase = random.randint(10, 50)
                    ferret_level_increase = random.randint(60, 200)
                    new_ferret_level = ferret_level + ferret_level_increase
                    # Оновлюємо рівень куниці та поінти в базі даних
                    cursor.execute("UPDATE users SET ferret_level=?, points=points+? WHERE id=?", (new_ferret_level, ferret_level_increase, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Куниця принесла пташку, яка підвищує рівень куниці на {bird_level_increase} і дарує вам {ferret_level_increase}🍪.")
                elif play_chance <= 80:
                    points_lost = random.randint(100, 400)
                    # Оновлюємо поінти в базі даних
                    cursor.execute("UPDATE users SET points=points-? WHERE id=?", (points_lost, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Куниця вас вкусила під час гри! Ви втрачаєте {points_lost}🍪.")
                elif play_chance <= 90:
                    points_lost = random.randint(100, 400)
                    # Оновлюємо поінти в базі даних
                    cursor.execute("UPDATE users SET points=points-? WHERE id=?", (points_lost, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Куниці не сподобалась іграшка, яку ви запропонували, і вона йде по своїм справам. Ви втрачаєте {points_lost}🍪.")
                else:
                    level_increase = random.randint(1, 10)
                    new_ferret_level = ferret_level + level_increase
                    # Оновлюємо рівень куниці в базі даних
                    cursor.execute("UPDATE users SET ferret_level=? WHERE id=?", (new_ferret_level, user_id))
                    conn.commit()
                    bot.send_message(message.chat.id, f"Куниці сподобалась іграшка, але вона йде грати сама. Рівень куниці підвищується на {level_increase}.")
                # Обновляем время последнего использования команды для пользователя
                cursor.execute("UPDATE users SET last_cof_time=? WHERE id=?", (datetime.now().isoformat(), user_id))
                conn.commit()
        else:
            bot.send_message(message.chat.id, 'У вас ще немає куниці, напишіть "купити_куницю" 🦊')



import time
import datetime
import datetime as dt

@bot.message_handler(func=lambda message: 'поєдинок' in message.text.lower())
def battle(message):
    user_id = message.from_user.id

    # Перевірка, чи пройшло достатньо часу з останнього відправлення команди
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_biy FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        if result is not None:
            last_biy = dt.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') if result[0] is not None else dt.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            current_time = dt.datetime.now()
            time_diff = current_time - last_biy
            if time_diff.total_seconds() < 20 * 60:
                bot.send_message(message.chat.id, 'Ви можете відправити команду раз в 20 хвилин.')
                return

    # Оновлення часу останнього відправлення команди
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE users SET last_biy=? WHERE id=?", (current_time, user_id))
    conn.commit()

    # Перевірка, чи є куниця у користувача
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT photo, kunica_name, ferret_level, karma, points FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            # Створення нового запису для користувача
            cursor.execute("INSERT INTO users (id, photo, kunica_name, ferret_level, karma, points) VALUES (?, ?, ?, ?, ?, ?)", (user_id, None, "Default Ferret", 1, 0, 0))
            conn.commit()
            result = cursor.fetchone()

        if not message.reply_to_message:
            bot.send_message(message.chat.id, 'Оберіть користувача, якого хочете покликати на поєдинок.')
            return

        if result is None or result[0] is None:
            bot.send_message(message.chat.id, 'У вас немає куниці. Напишіть "купити_куницю" 🦊')
            return

        # Отримання ID та імені другого користувача через відповідь на повідомлення
        replied_user_id = message.reply_to_message.from_user.id
        replied_user_name = message.reply_to_message.from_user.first_name

        # Перевірка, чи є куниця у другого користувача
        cursor.execute("SELECT photo, kunica_name, ferret_level, karma, points FROM users WHERE id=?", (replied_user_id,))
        replied_result = cursor.fetchone()
        if replied_result is None or replied_result[0] is None:
            bot.send_message(message.chat.id, f"{replied_user_name} немає куниці. 🦊")
            return

        # Відправлення повідомлення з випадковим фото та описом
        ferret_name = result[1]
        replied_ferret_name = replied_result[1]
        bot.send_message(message.chat.id, f"Куниця {ferret_name} та куниця {replied_ferret_name} щось не поділили між собою. 🦊")

        # Затримка 5 секунд
        time.sleep(5)

        # Генерація випадкової ймовірності
        play_chance = random.randint(1, 100)

        if play_chance <= 20:
            # Куниця А перемогла
            points_increase = random.randint(1, 20)
            karma_decrease = random.randint(1, 5)
            points_lost = random.randint(100, 500)

            # Оновлення значень для куниці А
            cursor.execute("UPDATE users SET points=points+?, karma=karma-? WHERE id=?", (points_increase, karma_decrease, user_id))

            # Оновлення значень для куниці Б
            cursor.execute("UPDATE users SET points=points-?, ferret_level=ferret_level-? WHERE id=?", (points_increase, random.randint(1, 5), replied_user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Поєдинок завершено! Куниця {ferret_name} перемогла куницю {replied_ferret_name} і отримала {points_increase}🍪, зменшила свою карму на {karma_decrease}✨")
        elif play_chance <= 40:
            # Куниця Б перемогла
            points_increase = random.randint(1, 20)
            karma_decrease = random.randint(1, 5)
            points_lost = random.randint(100, 500)

            # Оновлення значень для куниці Б
            cursor.execute("UPDATE users SET points=points+?, karma=karma-? WHERE id=?", (points_increase, karma_decrease, replied_user_id))

            # Оновлення значень для куниці А
            cursor.execute("UPDATE users SET points=points-?, ferret_level=ferret_level-? WHERE id=?", (points_increase, random.randint(1, 5), user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Поєдинок завершено! Куниця {replied_ferret_name} перемогла куницю {ferret_name} і отримала {points_increase}🍪, зменшила свою карму на {karma_decrease}✨")
        elif play_chance <= 50:
            # Куниця А відмовилась битися
            karma_increase = random.randint(2, 7)
            points_increase = random.randint(20, 100)

            # Оновлення значень для куниці А
            cursor.execute("UPDATE users SET karma=karma+?, points=points+? WHERE id=?", (karma_increase, points_increase, user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Куниця {ferret_name} відмовилась битися і отримала {karma_increase} ✨ та {points_increase} 🍪.")
        elif play_chance <= 60:
            # Куниця Б відмовилась битися
            karma_increase = random.randint(2, 7)
            points_increase = random.randint(20, 100)

            # Оновлення значень для куниці Б
            cursor.execute("UPDATE users SET karma=karma+?, points=points+? WHERE id=?", (karma_increase, points_increase, replied_user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Куниця {replied_ferret_name} відмовилась битися і отримала {karma_increase} ✨ та {points_increase} 🍪.")
        elif play_chance <= 65:
            # Куниця А вкусила господаря
            points_lost = random.randint(200, 700)
            level_increase = random.randint(1, 2)

            # Оновлення значень для куниці А
            cursor.execute("UPDATE users SET points=points-?, ferret_level=ferret_level+? WHERE id=?", (points_lost, level_increase, user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Куниця {ferret_name} вкусила господаря і втратила {points_lost} 🍪, але підвищила свій рівень на {level_increase}.")
        elif play_chance <= 70:
            # Куниця Б вкусила господаря
            points_lost = random.randint(200, 700)
            level_increase = random.randint(1, 2)

            # Оновлення значень для куниці Б
            cursor.execute("UPDATE users SET points=points-?, ferret_level=ferret_level+? WHERE id=?", (points_lost, level_increase, replied_user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Куниця {replied_ferret_name} вкусила господаря і втратила {points_lost} 🍪, але підвищила свій рівень на {level_increase}.")
        elif play_chance <= 75:
            # Обидві куниці вирішили гратися
            karma_increase = random.randint(4, 12)
            points_increase = random.randint(300, 1000)
            level_increase = random.randint(3, 8)

            # Оновлення значень для куниці А
            cursor.execute("UPDATE users SET karma=karma+?, points=points+?, ferret_level=ferret_level+? WHERE id=?", (karma_increase, points_increase, level_increase, user_id))

            # Оновлення значень для куниці Б
            cursor.execute("UPDATE users SET karma=karma+?, points=points+?, ferret_level=ferret_level+? WHERE id=?", (karma_increase, points_increase, level_increase, replied_user_id))

            conn.commit()

            # Відправлення повідомлення з результатом поєдинку
            bot.send_message(message.chat.id, f"Куниця {ferret_name} та куниця {replied_ferret_name} вирішили не битися, але вони гарно погралися і отримали {karma_increase} ✨, {points_increase} 🍪 та підвищили свій рівень на {level_increase}.")
        else:
            # Нічия
            bot.send_message(message.chat.id, "Поєдинок завершився нічиєю. Жодна куниця не перемогла.")

        conn.commit()



@bot.message_handler(func=lambda message: message.text.lower() == 'робота_лабораторія')
def work_lab(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Перевірка, чи минуло більше 2 годин з останньої роботи
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT work_time FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()

        if result is not None:
            work_time = dt.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
            current_time = dt.datetime.now()
            time_diff = current_time - work_time
            if time_diff.total_seconds() < 2 * 60 * 60:
                bot.send_message(chat_id, 'Ви вже працюєте. Зачекайте, щоб знову відправитися на роботу.')
                return

    # Оновлення часу останньої роботи
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE users SET work_time=? WHERE id=?", (current_time, user_id))
    conn.commit()

    # Record the work in the database
    cursor.execute("UPDATE users SET work_type=1, work_time=? WHERE id=?", (current_time, user_id))
    conn.commit()

    # Відправлення повідомлення
    bot.send_message(chat_id, 'Ви вирушили на роботу, поверніться через 2 години щоб побачити результат.')


@bot.message_handler(func=lambda message: message.text.lower() == 'робота_експедиція')
def work_expedition(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Перевірка, чи минуло більше 2 годин з останньої роботи
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT work_time FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()

        if result is not None:
            work_time = dt.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
            current_time = dt.datetime.now()
            time_diff = current_time - work_time
            if time_diff.total_seconds() < 2 * 60 * 60:
                bot.send_message(chat_id, 'Ви вже працюєте. Зачекайте, щоб знову відправитися на роботу.')
                return

    # Оновлення часу останньої роботи
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE users SET work_time=? WHERE id=?", (current_time, user_id))
    conn.commit()

    # Запис роботи в базу даних
    cursor.execute("UPDATE users SET work_type=2, work_time=? WHERE id=?", (current_time, user_id))
    conn.commit()

    # Відправлення повідомлення
    bot.send_message(chat_id, 'Ви вирушили на роботу, поверніться через 2 години щоб побачити результат.')

    # Запис роботи в базу даних
    cursor.execute("UPDATE users SET work_type=2, work_time=? WHERE id=?", (current_time, user_id))
    conn.commit()

@bot.message_handler(func=lambda message: message.text.lower() == 'завершити_роботу')
def finish_work(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Перевірка, чи минуло більше 2 годин з останньої роботи
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT work_type, work_time FROM users WHERE id=?", (user_id,))
        result = cursor.fetchone()
        if result is not None:
            work_type = result[0]
            work_time = dt.datetime.strptime(result[1], '%Y-%m-%d %H:%M:%S')
            current_time = dt.datetime.now()
            time_diff = current_time - work_time
            if time_diff.total_seconds() < 2 * 60 * 60:
                remaining_time = int(2 * 60 * 60 - time_diff.total_seconds())
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                bot.send_message(chat_id, f'Ще треба працювати {minutes} хвилин {seconds} секунд.')
                return

            # Оновлення часу останньої роботи
            current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE users SET work_time=? WHERE id=?", (current_time, user_id))
            conn.commit()

            # Перевірка типу роботи
            if work_type == 0:
                # Користувач не працює
                bot.send_message(chat_id, 'Ви не працюєте зараз.')
                return
            if work_type == 1:
                # Робота в лабораторії
                points = random.randint(700, 1600)
                message = ''
                if random.random() <= 0.2:
                    points_lost = random.randint(300, 800)
                    message = f'О ні! Під час роботи ви розбили лабораторний посуд і втратили {points_lost} 🍪'
                    cursor.execute("UPDATE users SET points=points-? WHERE id=?", (points_lost, user_id))
                else:
                    message = f'Ви завершили роботу в лабораторії та отримали {points} 🍪'
                    cursor.execute("UPDATE users SET points=points+? WHERE id=?", (points, user_id))
                bot.send_message(chat_id, message)
            elif work_type == 2:
                # Робота в експедиції
                points = random.randint(800, 2500)
                message = ''
                random_number = random.random()
                if random_number <= 0.2:
                    message = f'Експедиція пройшла вдало, ви знайшли рідкісного метелика та отримали за це {points} 🍪'
                elif random_number <= 0.4:
                    message = f'Експедиція пройшла вдало, ви отримали {points} 🍪'
                elif random_number <= 0.6:
                    points_lost = random.randint(300, 1600)
                    message = f'О ні! Експедиція не вдалась, ви загубили свій улюблений набір інструментів і втратили {points_lost} 🍪'
                    cursor.execute("UPDATE users SET points=points-? WHERE id=?", (points_lost, user_id))
                elif random_number <= 0.8:
                    points_lost = random.randint(200, 500)
                    message = f'О ні! Експедиція не вдалась, ви не впорались з роботою, яку вам довірили і втратили {points_lost} 🍪'
                    cursor.execute("UPDATE users SET points=points-? WHERE id=?", (points_lost, user_id))
                else:
                    message = 'Ви забули взяти обладнання, тому не змогли вирушити у експедицію!'
                bot.send_message(chat_id, message)

            conn.commit()


import random
import sqlite3
from datetime import datetime, timedelta

@bot.message_handler(content_types='text')
def addpoints(message):
    if message.text == "Топ_печиво":
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_karma_time INTEGER, last_reply_time INTEGER, kunica_name TEXT, photo TEXT)")

            cursor.execute("SELECT username, points FROM users ORDER BY points DESC LIMIT 10")
            result = cursor.fetchall()

            if result:
                text = 'Топ 10 печиво:\n'
                for i, row in enumerate(result):
                    name = row[0]
                    points = row[1]
                    text += f'{i+1}. {name}: {points}🍪\n'
                bot.send_message(message.chat.id, text)
            else:
                bot.send_message(message.chat.id, "Нет данных о печеньках")

        finally:
            cursor.close()
            conn.close()

    elif message.text == "Топ_карма":
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, karma INTEGER, points INTEGER, users INTEGER, last_command_time TIMESTAMP DEFAULT NULL, last_karma_time INTEGER, last_reply_time INTEGER, kunica_name TEXT, photo TEXT)")
            cursor.execute("SELECT username, karma FROM users ORDER BY karma DESC LIMIT 10")
            result = cursor.fetchall()

            if result:
                text = 'Топ 10 карма:\n'
                for i, row in enumerate(result):
                    name = row[0]
                    karma = row[1]
                    text += f'{i+1}. {name}: {karma}✨\n'
                bot.send_message(message.chat.id, text)
            else:
                bot.send_message(message.chat.id, "Нет данных о карме")

        finally:
            cursor.close()
            conn.close()


    for a in blacklist:
        if(a in message.text):
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(1)
            bot.send_message(
                message.chat.id, text="Налаштовую зв'язок з адміном.Очікуйте...")
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(3)
            bot.send_message(
                message.chat.id, text='Повідомлення відправленно.')
            bot.send_message('-1001880937482', 'Адміни,вам повідомлення від ' +
                             '@{username}\n'.format(username=message.from_user.username))
            chat_id = '-1001880937482'
    # Проверяем, что сообщение содержит текст
            if message.text:
                # Удаляем команду из сообщения
                text = message.text.replace('Forward', '')
        # Пересылаем сообщение
                bot.send_message(chat_id=chat_id, text=text)
    if(message.text == "Наступне питання"):
        test_handler(message)
    if(message.text == "Далі"):
        histology_test_handler(message)
    if(message.text == "Продовжити"):
        zoo_test(message)

    for b in hello:
        if(b in message.text.lower()):
            msg = random.choice(hellouser)
            probability = 0.01

            random_number = random.random()

            if random_number < probability:
                bot.reply_to(message, msg)

    for b in by:
        if(b in message.text.lower()):
            msg = random.choice(byuser)
            probability = 0.01

            random_number = random.random()

            if random_number < probability:
                bot.reply_to(message, msg)


photos = ['https://ru.files.fm/u/a3caa3rvs','https://ru.files.fm/f/z6ruwek8n', 'https://ru.files.fm/f/aw8ns8wvq', 'https://ru.files.fm/f/68hna3any', 'https://ru.files.fm/f/andaurk2a', 'https://ru.files.fm/f/z7dq5bvpv', 'https://ru.files.fm/f/3d59rb4fs','https://ru.files.fm/f/57w2g4xb4','https://ru.files.fm/f/5y8tmradp','https://ru.files.fm/f/6emc4vru5','https://ru.files.fm/f/zzgqxdnjd','https://ru.files.fm/f/nau28gt3a','https://ru.files.fm/f/sadncmag6','https://ru.files.fm/f/8tzzr5v5p']


blacklist = ['Forward' ]
by1 = ['Вітаємо вас у чаті біологів!','Раді бачити вас тут!','Ласкаво просимо до нашої спільноти біологів.','Вітаємо нового учасника!','Вітаємо вас у нашому чаті, де ми досліджуємо різноманітні аспекти біології.']
by2 = ['Дякуємо за вашу участь в нашому чаті.','Дякуємо за цікаві дискусії, було приємно з вами спілкуватися.','До побачення, дякуємо за вашу активну участь у нашому чаті.',' Дякуємо за вашу цікаву інформацію та досвід, який ви поділилися з нами. ','Було приємно спілкуватися з вами, дякуємо за вашу участь.','До побачення, дякуємо за вашу цікаву інформацію та допомогу в нашому чаті.']
msgpin = ['Це важлива інформація!','Якісь новини? зараз почитаємо...','Не забагато закріплених повідомлень?','А ось і важлива інформація','Кожен раз щось нове, я вже не встигаю це читати']
#повідомлення яке приймаємо
by = ['бувай','до зустрічі','скоро повернуся','скоро повернусь','зараз повернусь','зараз повернуся','до побачення']
hello = ['привіт','Доброго вечора! Ми з України','добрий день','доброго дня','доброго ранку','доброго вечора','добрий ранок','добрий вечір','доброго дня','ку','як справи','вітаю']
#відповідь на повідомлення
hellouser = ['Вітаю','Доброго вечора! Ми з України','Нічого оригінальнішого не придувам?','Добрий день','Я так радий тебе бачити!','Не забув про привітання, молодець','Знову повідомлення з цього чату, я навіть не встиг каву допити...','Бачу вас як наяву','Hello','Було так тихо поки ти не прийшов','Нарешті хтось прийшов! Ти навіть не уявляєш як я радий тебе бачити!','Давно тебе не було )','Я вже думав чат помер','Я так втомився вам відповідати','Так важко кожного разу вигадувати привітання']
byuser = ['Пока','Бувай','Сподіваюсь ми ще побачимося','Ти ж повернешся?','Мінус учасник розмови','Тепер буде тихіше','З кожною хвилиною людей у цьому чаті стає все меньше','От би й мені можна було піти з розмови','Приходь до нас ще','До зустрічі','Чекаю на твоє помідомлення']

bot.infinity_polling(timeout=10, long_polling_timeout = 5)
