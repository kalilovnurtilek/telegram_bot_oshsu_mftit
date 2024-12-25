 keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
        [InlineKeyboardButton(text="Help", callback_data="help")],
        [InlineKeyboardButton(text="Get Code", callback_data="get_code")],
        [InlineKeyboardButton(text="Send Picture", callback_data="send_picture")]
    ])