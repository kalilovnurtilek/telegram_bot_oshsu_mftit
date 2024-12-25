import asyncio
import logging
from aiogram import Bot, Dispatcher, types , F
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
    url = "https://cdn-icons-png.flaticon.com/512/4711/4711987.png"
    full_name = message.from_user.full_name or "Гость"

   

    await message.answer(
        parse_mode=ParseMode.HTML,
        text=f"""{markdown.hide_link(url)}Саламатсызбы, {markdown.hbold(full_name)}, мен МФТИТ тарабынан түзүлгөн жардамчы ботмун, эгерде жардам керек болсо төмөндөгү командаларды басыңыз
    /statement - Арыздардын үлгүлөрү
    /reference - Маалымкаттар (справка) боюнча маалымат
        """,
       
    )
    logging.info(f"/start обработан для пользователя {full_name}")

@dp.message(Command("statement"))
async def statemend_help(message:types.Message):
    logging.info("Обработан /start командой.")
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





@dp.message(Command("reference"))
async def statemend_help(message:types.Message):
    logging.info("Обработан /reference командой.")
    full_name = message.from_user.full_name or "Гость"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [InlineKeyboardButton(text="Академиялык өргүүгө чыгуу үчүн арыз", callback_data="help")],
        [InlineKeyboardButton(text="Академиялык өргүүдөн кайтуу үчүн арыз", callback_data="get_code")],
        [InlineKeyboardButton(text="Сабактардан уруксат сураа үчүн арыз", callback_data="send_picture")],
        [InlineKeyboardButton(text="Фамилияны avn ден өзгөртүү үчүн арыз", callback_data="send_picture")],
        [InlineKeyboardButton(text="вц", callback_data="send_picture")]

    ])

    await message.answer(
        text=f"Урматтуу , {markdown.hbold(full_name)},төмөндөгү арыздардын үлгүлөрү , өзүңүзгө керектүү арызды алсаңыз болот",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
    logging.info(f"/reference обработан для пользователя {full_name}")




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



# Эхо бот
@dp.message()
async def echo_message(message:types.Message):
    await message.answer(
        text="Wait a second..."
        )
    try:
        await message.forward(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text = "Somthing new ..")


@dp.message(F.photo, ~F.caption)
async def handle_photo_with_please_caption(message: types.Message):
    caption = "Извините я рне могу определить это фото"
    await message.reply_photo(
        photo=message.photo[-1].file_id,
        caption=caption, 
    )
any_media_filter = F.photo | F.video  | F.document



@dp.message(any_media_filter, ~F.caption)
async def handle_photo_wo_caption(message:types.Message):
    await message.reply("I can't see ")
    if message.document:    
            await message.reply_document(
            document=message.document.file_id)
    elif message.video:
            await message.reply_video(
                video = message.video.file_id
            )
    else:
            await message.reply("I can't see")
    

@dp.message(any_media_filter,F.caption)
async def handle_any_media_w_caption(message:types.Message):
    await message.reply(f"Smth in on media. Your text : {message.caption !r}")





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
