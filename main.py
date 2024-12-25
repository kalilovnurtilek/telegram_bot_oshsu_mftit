import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot_token

# Инициализация диспетчера
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
def db_connect():
    return sqlite3.connect('users.db')

# Создание таблицы для пользователей (если она не существует)
def create_table():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Добавление пользователя в базу данных
def add_user(user_id, full_name, username):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (id, full_name, username)
        VALUES (?, ?, ?)
    ''', (user_id, full_name, username))
    conn.commit()
    conn.close()

# Обработчик /start с кнопками
@dp.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    logging.info("Обработан /start командой.")
    url = "https://cdn-icons-png.flaticon.com/512/4711/4711987.png"
    full_name = message.from_user.full_name or "Гость"
    username = message.from_user.username or "Unknown"

    # Добавляем пользователя в базу данных
    add_user(message.from_user.id, full_name, username)

    await message.answer(
        parse_mode=ParseMode.HTML,
        text=f"""{markdown.hide_link(url)}Саламатсызбы, {markdown.hbold(full_name)}, мен МФТИТ тарабынан түзүлгөн жардамчы ботмун, эгерде жардам керек болсо төмөндөгү командаларды басыңыз
    /statement - Арыздардын үлгүлөрү
    /reference - Маалымкаттар (справка) боюнча маалымат
        """,
    )
    logging.info(f"/start обработан для пользователя {full_name}")

# Пример команды для получения информации из базы данных
@dp.message(Command("userinfo"))
async def user_info(message: types.Message):
    user_id = message.from_user.id
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT full_name, username, start_time FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        await message.answer(f"Информация о пользователе:\n\nИмя: {user[0]}\nИмя пользователя: {user[1]}\nДата регистрации: {user[2]}")
    else:
        await message.answer("Пользователь не найден в базе данных.")

# Другие обработчики команд
@dp.message(Command("statement"))
async def statemend_help(message: types.Message):
    logging.info("Обработан /statement командой.")
    full_name = message.from_user.full_name or "Гость"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [InlineKeyboardButton(text="Академиялык өргүүгө чыгуу үчүн арыз", url = "https://drive.google.com/file/d/1VLt9X84a0QcJFMWro4jTSUvypSJ51iL6/view?usp=sharing")],
        [InlineKeyboardButton(text="Академиялык өргүүдөн кайтуу үчүн арыз", url = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg")],
        [InlineKeyboardButton(text="Сабактардан уруксат сураа үчүн арыз", url = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg")],
        [InlineKeyboardButton(text="Фамилияны avn ден өзгөртүү үчүн арыз", url = "https://drive.google.com/file/d/1D7UGgqOACZoByGkjlJ3JdEHup11Hsm-P/view?usp=sharing")],
        [InlineKeyboardButton(text="Окуудан четтетүү үчүн арыз",url = "https://drive.google.com/file/d/1OBHGfo77DYpjefORGp_XoqnWctQLL_mX/view?usp=sharing")]
    ])
    await message.answer(
        text=f"Урматтуу , {markdown.hbold(full_name)},төмөндөгү арыздардын үлгүлөрү , өзүңүзгө керектүү арызды алсаңыз болот",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
    logging.info(f"/statement обработан для пользователя {full_name}")

# Основной метод запуска бота
async def main() -> None:
    bot = Bot(token=bot_token)
    create_table()  # Создаем таблицу при старте
    try:
        logging.info("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        logging.info("Бот остановлен.")

if __name__ == "__main__":
    asyncio.run(main())
