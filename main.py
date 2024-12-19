import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from magic_filter import F, RegexpMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from config import bot_token

dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик /start с кнопками
@dp.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    url = "https://w7.pngwing.com/pngs/332/245/png-transparent-robot-waving-hand-bot-robot-thumbnail.png"
    
    # Создаём клавиатуру с кнопками
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text="Help"))
    keyboard.add(types.KeyboardButton(text="Get Code"))
    keyboard.add(types.KeyboardButton(text="Send Picture"))
    keyboard.adjust(2)
    
    await message.answer(
        text=f"{markdown.hide_link(url)}Здравствуйте, {markdown.hbold(message.from_user.full_name)}, я ваш бот-помощник от дирекции МФТИТ ОшГУ",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )

# Обработчик /help с кнопками
@dp.message(Command("help"))
async def handle_help(message: types.Message) -> None:
    text = markdown.text(
        markdown.quote("I'm an echo bot."),
        markdown.bold("Send me"),
        markdown.underline("literally any message!"),
        sep='\n'
    )
    
    # Создаём клавиатуру для меню
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text="Back to Start"))
    keyboard.add(types.KeyboardButton(text="Get Code"))
    keyboard.add(types.KeyboardButton(text="Send Picture"))
    keyboard.adjust(2)
    
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard.as_markup(resize_keyboard=True),
    )

# Обработчик /code с префиксом /!%
@dp.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message) -> None:
    text = markdown.text(
        "Here's Python code:",
        markdown.pre("print('Hello world')\ndef foo():\n    return 'bar'"),
        sep="\n"
    )
    await message.answer(text=text)

# Обработчик /pic
@dp.message(Command("pic"))
async def handle_command_pic(message: types.Message) -> None:
    url = "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"
    await message.reply_photo(photo=url, caption="Here's a small cat picture!")

# Обработчик фото без подписи
@dp.message(F.photo & ~F.caption)
async def handle_photo_wo_caption(message: types.Message) -> None:
    caption = "Извините, я не могу определить это фото."
    await message.reply_photo(photo=message.photo[-1].file_id, caption=caption)

# Обработчик любых медиа
@dp.message(F.photo | F.video | F.document)
async def handle_any_media(message: types.Message) -> None:
    if message.document:
        await message.reply_document(document=message.document.file_id)
    elif message.video:
        await message.reply_video(video=message.video.file_id)
    else:
        await message.reply("Я не могу обработать это.")

# Обработчик для секрета (admin message)
@dp.message(F.text == "secret")
async def secret_admin_message(message: types.Message) -> None:
    await message.reply("Hi admin")

# Обработчик числового кода
@dp.message(F.text.regexp(r"\d+", mode=RegexpMode.FINDALL).as_("code"))
async def handle_code(message: types.Message, code: list[str]) -> None:
    await message.reply(f"Your code: {', '.join(code)}")

# Обработчик для эхо-сообщений
@dp.message()
async def echo_message(message: types.Message) -> None:
    try:
        await message.forward(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Что-то пошло не так...")

# Добавление кнопок для выбора числа (инлайн кнопки)
@dp.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)]
        ]
    )
    await message.answer(
        "Выберите число:",
        reply_markup=markup,
    )

# Обработчик для кнопок выбора чисел (инлайн)
@dp.callback_query(F.data.in_([str(i) for i in range(1, 6)]))
async def process_callback_number(callback: types.CallbackQuery):
    number = callback.data
    await callback.answer(f"Вы выбрали число: {number}")

async def main() -> None:
    bot = Bot(token=bot_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
