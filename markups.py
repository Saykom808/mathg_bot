import telebot
from telebot import types

# --Главное меню---

mainMenu = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
help_button = types.KeyboardButton('Правила ввода')
differentiate_button = types.KeyboardButton('Ввести производную')
game_button = types.KeyboardButton('Игра обучение')
mainMenu.add(help_button, differentiate_button, game_button)

# --Меню во время ввода производной---

stopMenu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
stop_button = types.KeyboardButton('Стоп')
stopMenu.add(stop_button)
