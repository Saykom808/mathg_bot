import logging
import telebot
from telebot import types
import markups as nav
from db import Database


token = '6618732731:AAHDw39S5cH3Of0IdaZ3sfXGfvoMipGVUf4'
youtoken = '381764678:TEST:76437'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Инициализируем базу данных
db = Database('database.db')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Укажите ваш ник')
    else:
        bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=nav.mainMenu)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def bot_message(message: telebot.types.Message):
    if message.chat.type == 'private':
        if message.text == "PROFILE":
          user_nickname = 'Your nickname' + " : " + db.get_nickname(message.from_user.id)
          bot.send_message(message.from_user.id, user_nickname)
        if message.text == "SUBSCRIBE":
          
          bot.send_message(message.from_user.id, 'Описание подписки', reply_markup=nav.sub_inline_markup)
        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if len(message.text) > 15:
                    bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов!")
                elif '@' in message.text or '/' in message.text:
                    bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "Done")
                    bot.send_message(message.from_user.id, "Регистрация прошла успешно!", reply_markup=nav.mainMenu)
            else:
                bot.send_message(message.from_user.id, "Перепроверьте запрос")

@bot.callback_query_handler(func=lambda message: True) 
def submonth(call: telebot.types.CallbackQuery):
  bot.sendmessage(call.from_user_id, title="Оформлена подписка", description="Тестовое описание товара", payloads='month_sub')

# Запускаем бот
if __name__=="__main__":
  bot.polling()
