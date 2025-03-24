import sqlite3  # Импортируем библиотеку для работы с SQLite базой данных
from calendar import monthcalendar  # Импортируем функцию для генерации календаря
from datetime import (
    datetime,
    timedelta,
)  # Импортируем модуль для работы с датой и временем

import telebot  # Импортируем библиотеку для работы с Telegram API
from dotenv import dotenv_values
from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    InlineKeyboardButton,
    CallbackQuery,
)

config = dotenv_values(".env")

# Импортируем необходимые типы из telebot для создания кнопок и обработки сообщений

bot = telebot.TeleBot(
    config.get("BOT_TOKEN")
)  # Создаем экземпляр Telegram-бота с указанным токеном
image_path = r"C:\Users\roman\AppData\Roaming\Telegram Desktop\photo_2025-03-24_15-50-12"  # Указываем путь к изображению (сырая строка для корректной обработки обратных слешей)
master_id = 1111853817
welcome_text = 'Привет! Я бот-помощник Мастера Виолетты @V_COBALT_V. Рад приветствовать! Как я могу помочь сегодня? (На данный момент я в стадии активной разработки и буду очень рад Вашей помощи с улучшением моей работы. В случае обнаружения любых неподалок или же ошибок, пожалуйста нажмите "Нашла ошибку" и подробно опишите ее. Виолетта и разработчики обязательно это увидят и сделаю все, чтобы исправить ошибку. Спасибо за ваше понимание и помощь, мы очень ценим это'


def get_db():
    con = sqlite3.connect(
        "Martini.db"
    )  # Подключаемся к базе данных (или создаем её, если она не существует)
    cur = con.cursor()  # Создаем курсор для выполнения SQL-запросов
    return con, cur  # Возвращаем соединение и курсор


def init_database():
    con, cur = get_db()  # Получаем соединение и курсор
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id longint, nickname string)"
    )  # Создаем таблицу users, если её нет (хранит данные о пользователях)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS entries(datetime timestemp, user_id longint, description text, istemporary "
        "boolean, isapproved boolean)"
    )  # Создаем таблицу entries, если её нет (хранит записи пользователей)
    con.commit()  # Сохраняем изменения в базе данных


init_database()  # Вызываем функцию для инициализации базы данных при запуске программы


@bot.message_handler(commands=["start", "help"])  # Обрабатываем команды /start и /help
def welcome_send(
    message: Message,
):  # Функция, которая вызывается при получении этих команд
    con, cur = get_db()
    res = cur.execute(f"SELECT * FROM entries")
    res = res.fetchall()
    print(res)
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )  # Создаем клавиатуру с адаптивным размером
    btm1 = KeyboardButton(
        "Записаться на коготочки"
    )  # Создаем кнопку "Записаться на коготочки"
    btm2 = KeyboardButton("Просмотр записей")  # Создаем кнопку "Просмотр записей"
    btm3 = KeyboardButton("Прайс")  # Создаем кнопку "Прайс"
    markup.add(btm1, btm2, btm3)  # Добавляем кнопки на клавиатуру
    bot.send_message(
        message.from_user.id, welcome_text, reply_markup=markup
    )  # Отправляем приветственное сообщение с клавиатурой


@bot.message_handler(content_types=["text"])  # Обрабатываем текстовые сообщения
def handler_text(
    message: Message,
):  # Функция, которая вызывается при получении текстового сообщения
    if (
        message.text == "Записаться на коготочки"
    ):  # Если пользователь нажал кнопку "Записаться на коготочки"
        bot.send_message(
            message.from_user.id, "Ща запишу"
        )  # Отправляем сообщение о начале записи
        datetime_now = datetime.now()  # Получаем текущую дату и время
        markup = InlineKeyboardMarkup()
        current_month = InlineKeyboardButton(
            datetime_now.strftime("%B"),
            callback_data=f"calendary|{datetime_now.month}",
        )
        datetime_now = datetime_now + timedelta(days=31)
        next_month = InlineKeyboardButton(
            datetime_now.strftime("%B"), callback_data=f"calendary|{datetime_now.month}"
        )
        markup.add(current_month, next_month)  # Добавляем кнопки на клавиатуру
        bot.send_message(
            message.from_user.id,
            "выберите месяц:",  # Предлагаем выбрать дату
            reply_markup=markup,  # Отправляем клавиатуру с календарем
        )
    elif (
        message.text == "Просмотр записей"
    ):  # Если пользователь нажал кнопку "Просмотр записей"
        bot.send_message(
            message.from_user.id, "Ща покажу"
        )  # Отправляем сообщение о просмотре записей
    elif message.text == "Прайс":  # Если пользователь нажал кнопку "Прайс"
        bot.send_message(
            message.from_user.id, "Ща ахуеешь"
        )  # Отправляем сообщение с ценами
        photo = open(
            "C:/Users/roman/AppData/Roaming/Telegram Desktop/photo_2025-03-24_15-50-12.jpg",
            "rb",
        )  # Открываем изображение в бинарном режиме
        bot.send_photo(
            message.from_user.id, photo
        )  # Отправляем изображение пользователю
    else:  # Если текст не соответствует ни одной кнопке
        con, cur = get_db()  # Подключаемся к базе данных
        res = cur.execute(
            f"SELECT * FROM entries WHERE user_id={message.from_user.id} and istemporary is TRUE"
        )  # Ищем временную запись пользователя
        res = res.fetchone()  # Получаем результат запроса
        if res is None:  # Если запись не найдена
            bot.send_message(
                message.from_user.id, "Вы чорт"
            )  # Отправляем сообщение об ошибке
            return
        cur.execute(
            f"UPDATE entries SET description = '{message.text}', istemporary = FALSE WHERE user_id={message.from_user.id} and istemporary is TRUE"
        )  # Обновляем временную запись, добавляя описание
        con.commit()  # Сохраняем изменения в базе данных
        bot.send_message(message.from_user.id, "Ваша запись на подтверждении")
        print(res)
        date = datetime.strptime(res[0], "%Y-%m-%d %H:%M:%S")
        markup = InlineKeyboardMarkup()
        approve = InlineKeyboardButton(
            "Подтвердить", callback_data=f"approve|{message.from_user.id}"
        )
        decline = InlineKeyboardButton(
            "Послать нахуй", callback_data=f"decline|{message.from_user.id}"
        )
        markup.add(approve, decline)  # Добавляем кнопки на клавиатуру
        bot.send_message(
            master_id,
            f"Требуется подтвердить запись \nДата записи: {date.strftime('%d-%m-%Y')}\nВремя записи: {date.strftime('%H-%M')}\nОписание: {message.text}",
            reply_markup=markup,
        )


@bot.callback_query_handler(
    func=lambda call: True
)  # Обрабатываем все нажатия на Inline-кнопки
def callback(call: CallbackQuery):  # Функция, которая вызывается при нажатии на кнопку
    datetime_now = datetime.now()  # Получаем текущую дату и время
    if call.data == "ignore":  # Если нажата кнопка "ignore" (пустая дата)
        return  # Игнорируем действие
    print(call.data)  # Выводим данные кнопки в консоль для отладки
    if (
        "day|" in call.data and "time|" not in call.data
    ):  # Если выбран день (но не выбрано время)
        temp = call.data.split(" ")
        day = temp[0].split("|")[1]
        month = temp[1].split("|")[1]
        bot.send_message(
            call.from_user.id,
            "Выберите время:",  # Предлагаем выбрать время
            reply_markup=create_entries(
                day, month
            ),  # Отправляем клавиатуру с временными слотами
        )
    elif "time|" in call.data:  # Если выбрано время
        temp = call.data.split(" ")  # Разбираем callback_data на части
        day = temp[0].split("|")[1]  # Получаем номер дня
        time = temp[1].split("|")[1]  # Получаем время
        month = int(temp[2].split("|")[1])
        data_time = datetime(
            year=datetime_now.year,
            month=month,
            day=int(day),
            hour=int(time.split(":")[0]),
            minute=int(time.split(":")[1]),
        )  # Формируем объект datetime для записи в базу данных
        con, cur = get_db()  # Подключаемся к базе данных
        res = cur.execute(
            f"SELECT user_id FROM entries WHERE datetime = '{data_time}'"
        ).fetchone()
        print(res)
        if res is not None:
            bot.send_message(call.from_user.id, "Время занято")
            return
        con, cur = get_db()  # Подключаемся к базе данных
        cur.execute(
            f"INSERT INTO entries (istemporary, user_id, datetime) VALUES(TRUE, {call.from_user.id}, '{data_time}')"
        )  # Добавляем временную запись в базу данных`
        con.commit()  # Сохраняем изменения
        bot.send_message(
            call.from_user.id, "Напишите ваши пожелания:"
        )  # Просим пользователя написать пожелания
    elif "back" in call.data:  # Если нажата кнопка "К выбору даты"
        datetime_now = datetime.now()  # Получаем текущую дату и время
        markup = InlineKeyboardMarkup()
        current_month = InlineKeyboardButton(
            datetime_now.strftime("%B"),
            callback_data=f"calendary|{datetime_now.month}",
        )
        datetime_now = datetime_now + timedelta(days=31)
        next_month = InlineKeyboardButton(
            datetime_now.strftime("%B"), callback_data=f"calendary|{datetime_now.month}"
        )
        markup.add(current_month, next_month)  # Добавляем кнопки на клавиатуру
        bot.send_message(
            call.from_user.id,
            "выберите месяц:",  # Предлагаем выбрать дату
            reply_markup=markup,  # Отправляем клавиатуру с календарем
        )
    elif "approve" in call.data:
        user_id = call.data.split("|")[1]
        con, cur = get_db()  # Подключаемся к базе данных
        cur.execute(f"UPDATE entries SET isapproved = TRUE WHERE user_id={user_id}")
        con.commit()  # Сохраняем изменения в базе данных
        bot.send_message(int(user_id), "Ваша запись подтверждена")
    elif "decline" in call.data:
        user_id = call.data.split("|")[1]
        con, cur = get_db()  # Подключаемся к базе данных
        cur.execute(
            f"DELETE FROM entries WHERE user_id={user_id} and isapproved is NOT TRUE"
        )
        con.commit()  # Сохраняем изменения в базе данных
        bot.send_message(int(user_id), "Вы пошли нахуй")
    elif "calendary" in call.data:
        month = int(call.data.split("|")[1])
        print(month)
        datetime_now = datetime.now()
        bot.send_message(
            call.from_user.id,
            "Выберите дату:",
            reply_markup=create_calendar(year=datetime_now.year, month=month),
        )


def create_calendar(year, month):
    markup = InlineKeyboardMarkup()  # Создаем Inline-клавиатуру
    cal = monthcalendar(year, month)  # Получаем календарь на указанный месяц
    days_of_week = [
        "Пн",
        "Вт",
        "Ср",
        "Чт",
        "Пт",
        "Сб",
        "Вс",
    ]  # Создаем список дней недели
    week_buttons = []
    for day in days_of_week:
        week_buttons.append(
            InlineKeyboardButton(day, callback_data="ignore")
        )  # Добавляем кнопки дней недели
    markup.row(*week_buttons)  # Добавляем строку с днями недели
    for week in cal:  # Проходим по каждой неделе месяца
        week_buttons = []
        for day in week:  # Проходим по каждому дню недели
            text = day
            call = f"day|{day} month|{month}"  # Формируем callback_data для кнопки
            if day == 0:  # Если день равен 0 (пустой слот)
                text = " "
                call = "ignore"  # Устанавливаем callback_data на "ignore"
            week_buttons.append(
                InlineKeyboardButton(text, callback_data=str(call))
            )  # Добавляем кнопку
        markup.row(*week_buttons)  # Добавляем строку с кнопками
    return markup  # Возвращаем созданную клавиатуру


def create_entries(day, month):
    markup = InlineKeyboardMarkup()  # Создаем Inline-клавиатуру
    entries = ["10:00", "13:00", "16:00", "19:00"]  # Список временных слотов
    hour_buttons = []
    for time in entries:
        hour_buttons.append(
            InlineKeyboardButton(
                time, callback_data=f"day|{day} time|{time} month|{month}"
            )
        )  # Добавляем кнопки
    markup.row(*hour_buttons)  # Добавляем строку с временными слотами
    markup.row(
        InlineKeyboardButton(text="К выбору даты", callback_data="back")
    )  # Добавляем кнопку "К выбору даты"
    return markup  # Возвращаем созданную клавиатуру


bot.infinity_polling()  # Запускаем бота в режиме постоянного опроса сервера Telegram
