# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import telebot
from telebot import types
#--Main Menu ---

mainMenu = types.ReplyKeyboardMarkup(row_width=1)
profile_button = types.KeyboardButton('PROFILE')
subscribe_button = types.KeyboardButton('SUBSCRIBE')
mainMenu.add(profile_button, subscribe_button)

#--- SubInlineMenu ---

sub_inline_markup = types.InlineKeyboardMarkup(row_width=1)
# subscribe_month_2 = types.InlineKeyboardButton(text = "Месяц - 1 рубль", callback_data="submonth")
# sub_inline_markup.add(subscribe_month_2)