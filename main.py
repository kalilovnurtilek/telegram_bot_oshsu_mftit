import asyncio
import logging

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode , parse_mode
from config import bot_token 


dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    url = "https://w7.pngwing.com/pngs/332/245/png-transparent-robot-waving-hand-bot-robot-thumbnail.png"
    await message.answer(
        text=f"{markdown.hide_link(url)}Hello , {markdown.hbold( message.from_user.full_name)}",
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

any_media_filter = F.photo | F.video  | F.document



@dp.message(any_media_filter, ~F.caption)
async def handle_photo_wo_caption(message:types.Message):
    await message.reply("I can't see ")

@dp.message(F.photo ,F.caption.contains("please"))
async def handle_message(message:types.Message):
    await message.reply("I can't see , sorry . Could you describe it please")

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

