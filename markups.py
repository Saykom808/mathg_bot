import telebot
from telebot import types

#--Main Menu ---

mainMenu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
help_button = types.KeyboardButton('HELP')
integrate_button = types.KeyboardButton('INTEGRATE')
definite_integral_button = types.KeyboardButton('DEFINITE INTEGRAL')
mainMenu.add(help_button, integrate_button, definite_integral_button)

#--- SubInlineMenu ---

# Если нужны inline кнопки, можно добавить их здесь
# sub_inline_markup = types.InlineKeyboardMarkup(row_width=1)
# subscribe_month_2 = types.InlineKeyboardButton(text="Месяц - 1 рубль", callback_data="submonth")
# sub_inline_markup.add(subscribe_month_2)
