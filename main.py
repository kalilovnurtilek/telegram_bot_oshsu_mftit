import asyncio
import logging
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

# Обработчик /start с кнопками
@dp.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    logging.info("Обработан /start командой.")
    url = "https://w7.pngwing.com/pngs/332/245/png-transparent-robot-waving-hand-bot-robot-thumbnail.png"
    full_name = message.from_user.full_name or "Гость"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [InlineKeyboardButton(text="Help", callback_data="help")],
        [InlineKeyboardButton(text="Get Code", callback_data="get_code")],
        [InlineKeyboardButton(text="Send Picture", callback_data="send_picture")]
    ])

    await message.answer(
        text=f"{markdown.hide_link(url)}Здравствуйте, {markdown.hbold(full_name)}, я ваш бот-помощник от дирекции МФТИТ ОшГУ",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
    logging.info(f"/start обработан для пользователя {full_name}")

# Обработчик команды /help
@dp.message(Command("help"))
async def handle_help_command(message: types.Message) -> None:
    logging.info("Обработан /help командой.")
    await message.answer("Help command received!")

# Обработчик callback кнопки 'Help'
@dp.callback_query(lambda c: c.data == "help")
async def handle_help_callback(callback: types.CallbackQuery) -> None:
    logging.info("Обработан callback для кнопки 'Help'.")
    await callback.message.answer("Help callback received!")
    await callback.answer()

# Обработчик кнопки "Get Code"
@dp.callback_query(lambda c: c.data == "get_code")
async def handle_get_code(callback: types.CallbackQuery) -> None:
    logging.info("Обработан callback для кнопки 'Get Code'.")
    await callback.message.answer("Here is the Python code: `print('Hello world')`")
    await callback.answer()

# Обработчик кнопки "Send Picture"
@dp.callback_query(lambda c: c.data == "send_picture")
async def handle_send_picture(callback: types.CallbackQuery) -> None:
    logging.info("Обработан callback для кнопки 'Send Picture'.")
    url = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"
    await callback.message.answer_photo(photo=url, caption="Here's a small cat picture!")
    await callback.answer()

# Основной метод запуска бота
async def main() -> None:
    bot = Bot(token=bot_token)
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
