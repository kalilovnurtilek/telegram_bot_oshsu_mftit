import asyncio
import logging

from magic_filter import RegexpMode
from re import Match
from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode , parse_mode
from config import bot_token 
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardButton


dp = Dispatcher()

@dp.message(CommandStart()) 
async def handle_start(message: types.Message):
 
    url = "https://w7.pngwing.com/pngs/332/245/png-transparent-robot-waving-hand-bot-robot-thumbnail.png"
    await message.answer(
        text=f"{markdown.hide_link(url)}Здравствуйте , {markdown.hbold( message.from_user.full_name)}, я ваш бот помощник от дирекции МФТИТ ОшГУ",
        parse_mode= ParseMode.HTML,
        )
@dp.message(Command('help'))
async def handle_help(message: types.Message):
    
    # await message.answer(text='Сиз өзүңүзгө керектүү маалыматты ала аласыз')
    # text = "I'm an echo bot.\nSend me any message"    
    # entity_bold = types.MessageEntity(
    #     type = 'bold',
    #     offset = len("I'm an echo bot.\nSend me"),
    #     length = 3,
    # # )
    # entities = [entity_bold]
    # await message.answer(text=text, entities=entities)
    text = markdown.text(
        markdown.markdown_decoration.quote
        ("I'm an echo bot."),
       markdown.text(
       "Send me",
       markdown.markdown_decoration.bold(
       markdown.text(
       markdown.underline("litaralli"),
        ("any"),
        markdown.markdown_decoration.quote("message!"),
        ),
        ),
        sep ='\n',
    ))
    await message.answer(
        text =text,
        # parse_mode=None ,
        parse_mode = ParseMode.MARKDOWN_V2
        )

@dp.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message):
    text= markdown.text(
        "Here's Python code",
        "",
        markdown.markdown_decoration.pre(
            markdown.text(
                "print('Hello world)",
                "\n",
                "def foo():\n return 'bar' ",
                sep= "\n",
            )
        ),
        sep= "\n",
    )
    await message.answer(text=text)
@dp.message(Command("code"))
async def handle_command_code(message:types.Message):
    text = markdown.text(
        "Here is Python code",
        
        markdown.marcdown_decoration.pre_language(
            "print('Hello world')",
            language= "python"
            ) , 
        sep="\n"
         )
    await message.answer(text=text)

# def is_photo(message:types.Message):
#     if not message.photo:
#         return False
#     if not message.caption:
#         return False
#     return "please" in message .caption

@dp.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    url="https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"
    await message.reply_photo(
        photo=url,
        caption ="Cat small pic", )


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

@dp.message(F.text == "secret")
# F.from_user.id.in_({42 ,990282097}), 

async def secret_admin_message(message: types.Message):
    print(message.from_user.id)
    await message.reply("Hi admin")
    
@dp.message(F.text.regexp(r"(\d+),mode=RegexpMode.FINDALL").as_("code"))
async def handle_code(message:types.Message , code : list[str]):
    await message.reply(f"Your code :{code}")
@dp.message()
async def echo_message(message:types.Message):
    # await message.bot.send_message(
    #     chat_id= message.chat.id,
    #     text="Start processing...",
    # )
    # await message.bot.send_message(
    #   chat_id= message.chat.id,
    #   text="Detected message...",
    #   reply_to_message_id= message.message_id,  
    # )
   
    await message.answer(
        text="Wait a second..."
        )
     
    # if message.text:
    #     await message.answer(
    #         text = message.text,
    #         entities=message.entities,
    #     )
    try:
        # await message.copy_to(chat_id=message.chat.id)
        await message.forward(chat_id=message.chat.id)
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text = "Somthing new ..")
   
async def main():
    bot = Bot(
    token=bot_token,
    # parse_mode = ParseMode.MARKDOWN_V2,
    
    )
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

   