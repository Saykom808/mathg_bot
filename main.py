import logging
import telebot
from telebot import types
import markups as nav
from calc import integrate_function, definite_integral, differentiate_function
import re

token = '6618732731:AAHDw39S5cH3Of0IdaZ3sfXGfvoMipGVUf4'
# youtoken = '381764678:TEST:76437'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.from_user.id, 'Привет! Я бот-калькулятор интегралов и производных. Введите команду /help для получения списка команд.', reply_markup=nav.mainMenu)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    help_text = (
        "Команды:\n"
        "/differentiate - Вычисление производной\n"
    )
    bot.send_message(message.from_user.id, help_text, reply_markup=nav.mainMenu)

# Валидация выражения
def validate_expression(expression):
    pattern = r'^[0-9a-zA-Z+\-*/^() x]*$'
    return re.match(pattern, expression) is not None

# Обработчик команды /integrate
@bot.message_handler(commands=['integrate'])
def integrate(message: telebot.types.Message):
    msg = bot.send_message(message.from_user.id, "Введите выражение для интегрирования (например, x**2):")
    bot.register_next_step_handler(msg, get_expression)

def get_expression(message: telebot.types.Message):
    expression = message.text
    if validate_expression(expression):
        msg = bot.send_message(message.from_user.id, "Введите переменную интегрирования (например, x):")
        bot.register_next_step_handler(msg, get_variable, expression)
    else:
        bot.send_message(message.from_user.id, "Некорректное выражение. Попробуйте снова.", reply_markup=nav.mainMenu)

def get_variable(message: telebot.types.Message, expression):
    variable = message.text
    if variable.isalpha():
        try:
            result = integrate_function(expression, variable)
            bot.send_message(message.from_user.id, f"Неопределенный интеграл {expression} по {variable}: {result}", reply_markup=nav.mainMenu)
        except Exception as e:
            bot.send_message(message.from_user.id, f"Ошибка: {e}", reply_markup=nav.mainMenu)
    else:
        bot.send_message(message.from_user.id, "Некорректная переменная. Попробуйте снова.", reply_markup=nav.mainMenu)

# Обработчик команды /definite_integral
@bot.message_handler(commands=['definite_integral'])
def definite_integral_command(message: telebot.types.Message):
    msg = bot.send_message(message.from_user.id, "Введите выражение для интегрирования (например, x**2):")
    bot.register_next_step_handler(msg, get_definite_expression)

def get_definite_expression(message: telebot.types.Message):
    expression = message.text
    if validate_expression(expression):
        msg = bot.send_message(message.from_user.id, "Введите переменную интегрирования (например, x):")
        bot.register_next_step_handler(msg, get_definite_variable, expression)
    else:
        bot.send_message(message.from_user.id, "Некорректное выражение. Попробуйте снова.", reply_markup=nav.mainMenu)

def get_definite_variable(message: telebot.types.Message, expression):
    variable = message.text
    if variable.isalpha():
        msg = bot.send_message(message.from_user.id, "Введите нижний предел интегрирования:")
        bot.register_next_step_handler(msg, get_lower_limit, expression, variable)
    else:
        bot.send_message(message.from_user.id, "Некорректная переменная. Попробуйте снова.", reply_markup=nav.mainMenu)

def get_lower_limit(message: telebot.types.Message, expression, variable):
    try:
        lower_limit = float(message.text)
        msg = bot.send_message(message.from_user.id, "Введите верхний предел интегрирования:")
        bot.register_next_step_handler(msg, get_upper_limit, expression, variable, lower_limit)
    except ValueError:
        bot.send_message(message.from_user.id, "Неверный формат. Пожалуйста, введите число.", reply_markup=nav.mainMenu)

def get_upper_limit(message: telebot.types.Message, expression, variable, lower_limit):
    try:
        upper_limit = float(message.text)
        try:
            result = definite_integral(expression, variable, lower_limit, upper_limit)
            bot.send_message(message.from_user.id, f"Определенный интеграл {expression} по {variable} от {lower_limit} до {upper_limit}: {result}", reply_markup=nav.mainMenu)
        except Exception as e:
            bot.send_message(message.from_user.id, f"Ошибка: {e}", reply_markup=nav.mainMenu)
    except ValueError:
        bot.send_message(message.from_user.id, "Неверный формат. Пожалуйста, введите число.", reply_markup=nav.mainMenu)

# Обработчик команды /differentiate
@bot.message_handler(commands=['differentiate'])
def differentiate(message: telebot.types.Message):
    msg = bot.send_message(message.from_user.id, "Введите выражение для дифференцирования (например, x**2):")
    bot.register_next_step_handler(msg, get_diff_expression)

def get_diff_expression(message: telebot.types.Message):
    expression = message.text
    if validate_expression(expression):
        msg = bot.send_message(message.from_user.id, "Введите переменную дифференцирования (например, x):")
        bot.register_next_step_handler(msg, get_diff_variable, expression)
    else:
        bot.send_message(message.from_user.id, "Некорректное выражение. Попробуйте снова.", reply_markup=nav.mainMenu)

def get_diff_variable(message: telebot.types.Message, expression):
    variable = message.text
    if variable.isalpha():
        try:
            result = differentiate_function(expression, variable)
            bot.send_message(message.from_user.id, f"Производная {expression} по {variable} = {result}", reply_markup=nav.mainMenu)
        except Exception as e:
            bot.send_message(message.from_user.id, f"Ошибка: {e}", reply_markup=nav.mainMenu)
    else:
        bot.send_message(message.from_user.id, "Некорректная переменная. Попробуйте снова.", reply_markup=nav.mainMenu)

# Обработчик текстовых сообщений для кнопок
@bot.message_handler(func=lambda message: message.text in ['HELP', 'INTEGRATE', 'DEFINITE INTEGRAL', 'DIFFERENTIATE'])
def handle_buttons(message: telebot.types.Message):
    if message.text == 'HELP':
        help(message)
    elif message.text == 'INTEGRATE':
        integrate(message)
    elif message.text == 'DEFINITE INTEGRAL':
        definite_integral_command(message)
    elif message.text == 'DIFFERENTIATE':
        differentiate(message)

# Запускаем бот
if __name__ == "__main__":
    bot.polling()
