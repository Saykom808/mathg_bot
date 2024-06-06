import telebot
from telebot import types

#--Main Menu ---

mainMenu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
help_button = types.KeyboardButton('HELP')

differentiate_button = types.KeyboardButton('DIFFERENTIATE')
mainMenu.add(help_button, differentiate_button)
