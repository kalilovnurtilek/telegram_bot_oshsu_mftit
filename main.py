import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT,
            feedback TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

# Добавление обратной связи в базу данных
def add_feedback(user_id, full_name, feedback):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (user_id, full_name, feedback)
        VALUES (?, ?, ?)
    ''', (user_id, full_name, feedback))
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

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сунуш, арыздарыныз болсо ушул баскычты басып калтырыңыз", callback_data="feedback")],
        [InlineKeyboardButton(text="Маалымкаттар (справка)", callback_data="reference")],
        [InlineKeyboardButton(text="Арыздардын үлгүлөрү", callback_data="statement")]
    ])

    await message.answer(
        parse_mode=ParseMode.HTML,
        text=f"""{markdown.hide_link(url)}Саламатсызбы, {markdown.hbold(full_name)}, мен МФТИТ тарабынан түзүлгөн жардамчы ботмун, эгерде жардам керек болсо төмөндөгү командаларды басыңыз""",
        reply_markup=keyboard
    )
    logging.info(f"/start обработан для пользователя {full_name}")

# Обработчик обратной связи
@dp.callback_query(lambda c: c.data == "feedback")
async def handle_feedback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Сунуш-арыздарды калтырыңыз...")

    @dp.message()
    async def get_feedback(message: types.Message):
        full_name = message.from_user.full_name or "Гость"
        add_feedback(message.from_user.id, full_name, message.text)
        await message.answer("Чоон рахмат , сиздин жазгандарыңыз маалыматтар базасында сакталып калды!")

# Обработчик справок
@dp.callback_query(lambda c: c.data == "reference")
async def reference_help(callback_query: types.CallbackQuery):
    full_name = callback_query.from_user.full_name or "Гость"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [InlineKeyboardButton(text="Каникулярдык справка", callback_data="spravka_k" )],
        [InlineKeyboardButton(text="Окуп жатканын тастыктоочу справка ",callback_data="spravka_k2")],
    ])
    await callback_query.message.answer(
        text=f"Урматтуу , {markdown.hbold(full_name)},маалымкаттарды чыгаруу боюнча маалыматтар бул жерде",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
    logging.info(f"/reference обработан для пользователя {full_name}")


@dp.callback_query(lambda c: c.data == "spravka_k2")
async def statement_help(callback_query: types.CallbackQuery):
    full_name = callback_query.from_user.full_name or "Гость"
    
    await callback_query.message.answer(
        text=f"Урматтуу , {markdown.hbold(full_name)},окуп жаткандыгын тастыктоочу справканын сиз башкы корпустун 301-кабинетинен ала аласыз",
        parse_mode=ParseMode.HTML,
    )
    logging.info(f"/statement обработан для пользователя {full_name}")




@dp.callback_query(lambda c: c.data == "spravka_k")
async def statement_help(callback_query: types.CallbackQuery):
    full_name = callback_query.from_user.full_name or "Гость"
    
    await callback_query.message.answer(
        text=f"Урматтуу , {markdown.hbold(full_name)},каникулярдык справканын үлгүлөрүн ушул шилтеме аркылуу ала аласыз https://drive.google.com/file/d/1VLt9X84a0QcJFMWro4jTSUvypSJ51iL6/view?usp=sharing",
        parse_mode=ParseMode.HTML,
    )
    logging.info(f"/statement обработан для пользователя {full_name}")











# Обработчик образцов заявлений
@dp.callback_query(lambda c: c.data == "statement")
async def statement_help(callback_query: types.CallbackQuery):
    full_name = callback_query.from_user.full_name or "Гость"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [InlineKeyboardButton(text="Академиялык өргүүгө чыгуу үчүн арыз", url="https://drive.google.com/file/d/1VLt9X84a0QcJFMWro4jTSUvypSJ51iL6/view?usp=sharing")],
        [InlineKeyboardButton(text="Академиялык өргүүдөн кайтуу үчүн арыз", url="https://docs.google.com/document/d/1rQ2H40e2rXUZfLBfnCR70bqS3AqhmjXD/edit?usp=sharing&ouid=112907680449529887487&rtpof=true&sd=true")],
        [InlineKeyboardButton(text="Сабактардан уруксат сураа үчүн арыз", url="https://docs.google.com/document/d/1BdkDy2oc20YBbuzj1rhByXenZo9-IVGL/edit?usp=sharing&ouid=112907680449529887487&rtpof=true&sd=true")],
        [InlineKeyboardButton(text="Фамилияны avn ден өзгөртүү үчүн арыз", url="https://drive.google.com/file/d/1D7UGgqOACZoByGkjlJ3JdEHup11Hsm-P/view?usp=sharing")],
        [InlineKeyboardButton(text="Окуудан четтетүү үчүн арыз", url="https://drive.google.com/file/d/1OBHGfo77DYpjefORGp_XoqnWctQLL_mX/view?usp=sharing")]
    ])
    await callback_query.message.answer(
        text=f"Урматтуу , {markdown.hbold(full_name)},төмөндөгү арыздардын үлгүлөрү , өзүңүзгө керектүү арызды алсаңыз болот",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
    logging.info(f"/statement обработан для пользователя {full_name}")



# @dp.message(F.text)
# async def echo_message(message: types.Message):
#     await message.answer(
#         text="Wait a second..."
#         )
#     url = "https://cdn-icons-png.flaticon.com/512/4711/4711987.png"
#     full_name = message.from_user.full_name or "Гость"
#     username = message.from_user.username or "Unknown"

#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Сунуш, арыздарыныз болсо ушул баскычты басып калтырыңыз", callback_data="feedback")],
#         [InlineKeyboardButton(text="Маалымкаттар (справка)", callback_data="reference")],
#         [InlineKeyboardButton(text="Арыздардын үлгүлөрү", callback_data="statement")]
#     ])

#     await message.answer(
#         parse_mode=ParseMode.HTML,
#         text=f"""{markdown.hide_link(url)}Урматтуу, {markdown.hbold(full_name)}, мен МФТИТ тарабынан түзүлгөн жардамчы ботмун, эгерде жардам керек болсо төмөндөгү командаларды басыңыз 
# {message.text}-бул сөздү биздин бот тааныган жок""",
#         reply_markup=keyboard
#     )
#     logging.info(f"/start обработан для пользователя {full_name}") 


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