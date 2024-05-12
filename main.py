import logging
import telebot
from telebot import types
import markups as nav
from db import Database

token = '6618732731:AAHDw39S5cH3Of0IdaZ3sfXGfvoMipGVUf4'
# youtoken = '381764678:TEST:76437'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Инициализируем базу данных
db = Database('database.db')

def days_to_seconds(days):
   return days * 24 * 60 * 60

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Привет! Укажите ваш ник')
    else:
        bot.send_message(message.from_user.id, "Вы уже зарегистрированы!", reply_markup=nav.mainMenu)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def bot_message(message: telebot.types.Message):
    if message.chat.type == 'private':
        if message.text == "PROFILE":
            if db.user_exists(message.from_user.id):
                user_nickname = 'Ваш ник: ' + db.get_nickname(message.from_user.id)
                bot.send_message(message.from_user.id, user_nickname)
            else:
                bot.send_message(message.from_user.id, "Вы еще не зарегистрированы.")
        elif message.text == "SUBSCRIBE":
            bot.send_message(message.chat.id, "Чтобы оформить подписку, нажмите кнопку оплаты:", reply_markup=nav.sub_inline_markup)
        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if len(message.text) > 15:
                    bot.send_message(message.from_user.id, "Никнейм не должен превышать 15 символов!")
                elif '@' in message.text or '/' in message.text:
                    bot.send_message(message.from_user.id, "Никнейм содержит запрещенные символы")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "Done")
                    bot.send_message(message.from_user.id, "Регистрация прошла успешно!", reply_markup=nav.mainMenu)
            else:
                bot.send_message(message.from_user.id, "Перепроверьте запрос")

# Обработчик callback-запросов для подписки
@bot.callback_query_handler(func=lambda call: call.data == "month_sub")
def process_subscription(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Оформлена подписка")

# Обработчик предварительных запросов на оплату
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Обработчик успешной оплаты
@bot.message_handler(content_types=["successful_payment"])
def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "month_sub":
        # Подписка пользователю
        bot.send_message(message.from_user.id, "Вам выдана подписка на месяц")

# Запускаем бот
if __name__ == "__main__":
    bot.polling()
