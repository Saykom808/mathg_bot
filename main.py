import logging
import telebot
from telebot import types
import markups as nav
from calc import differentiate_function
import re
import random

token = '7088961331:AAF1OdiZbup-63WanqRvlgh1s05uL9r6PgQ'
# token = 'TOKEN'
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(token)


derivatives_table = {
    'c': '0',
    'x**n': 'n*x**(n-1)',
    'a**x': 'a**x * log(a)',
    'e**x': 'e**x',
    'log(a, x)': '1 / (x * ln(a))',
    'ln(x)': '1 / x',
    'sin(x)': 'cos(x)',
    'cos(x)': '-sin(x)',
    'sqrt(x)': '1 / (2 * sqrt(x))',
    'tg(x)': '1 / cos(x)**2',
    'ctg(x)': '-1 / sin(x)**2',
    'c*u': 'c*u\'',
    'u + v': 'u\' + v\'',
    'u * v': 'u\' * v + u * v\'',
    'u / v': '(u\' * v - u * v\') / v**2'

}

current_game = {}

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.from_user.id, 'Привет! Я бот-калькулятор интегралов и производных. Введите команду /help для получения списка команд.', reply_markup=nav.mainMenu)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    help_text = (
        "Команды:\n"
        "/differentiate - Вычисление производной\n\n"
        "Правила ввода:\n"
        "1. Выражения должны быть корректными математическими выражениями.\n"
        "2. Используйте стандартные операторы: +, -, *, /, ** (для возведения в степень).\n"
        "3. Для квадратного корня используйте sqrt. Например, sqrt(x).\n"
        "4. Для экспоненты используйте exp. Например, exp(x).\n"
        "5. Для логарифмов используйте log. Например, log(x).\n"
        "6. Для тригонометрических функций используйте sin, cos, tan и т.д. Например, sin(x), cos(x).\n"
        "7. Переменные должны состоять из букв.\n"
        "Примеры корректных выражений:\n"
        "x**2 + 2*x + 1\n"
        "sqrt(x) + exp(x)\n"
        "sin(x) * cos(x)\n"
    )
    bot.send_message(message.from_user.id, help_text, reply_markup=nav.mainMenu)

def validate_expression(expression):
    pattern = r'^[0-9a-zA-Z+\-*/^() sqrt exp log sin cos tan]*$'
    return re.match(pattern, expression) is not None

@bot.message_handler(commands=['differentiate'])
def differentiate(message: telebot.types.Message):
    msg = bot.send_message(message.from_user.id, "Введите выражение для дифференцирования (например, x**2):", reply_markup=nav.stopMenu)
    bot.register_next_step_handler(msg, get_diff_expression)

def get_diff_expression(message: telebot.types.Message):
    if message.text.lower() == 'стоп':
        bot.send_message(message.from_user.id, "Возвращаемся в главное меню.", reply_markup=nav.mainMenu)
        return

    expression = message.text
    if validate_expression(expression):
        msg = bot.send_message(message.from_user.id, "Введите переменную дифференцирования (например, x):", reply_markup=nav.stopMenu)
        bot.register_next_step_handler(msg, get_diff_variable, expression)
    else:
        bot.send_message(message.from_user.id, "Некорректное выражение. Попробуйте снова.", reply_markup=nav.stopMenu)
        differentiate(message)

def get_diff_variable(message: telebot.types.Message, expression):
    if message.text.lower() == 'стоп':
        bot.send_message(message.from_user.id, "Возвращаемся в главное меню.", reply_markup=nav.mainMenu)
        return

    variable = message.text
    if variable.isalpha():
        try:
            result = differentiate_function(expression, variable)
            bot.send_message(message.from_user.id, f"Производная {expression} по {variable}: {result}", reply_markup=nav.mainMenu)
        except Exception as e:
            bot.send_message(message.from_user.id, f"Ошибка: Некорректный ввод", reply_markup=nav.stopMenu)
            differentiate(message)
    else:
        bot.send_message(message.from_user.id, "Некорректная переменная. Попробуйте снова.", reply_markup=nav.stopMenu)
        differentiate(message)

@bot.message_handler(func=lambda message: message.text == 'Правила ввода')
def handle_help_button(message: telebot.types.Message):
    help(message)

@bot.message_handler(func=lambda message: message.text == 'Ввести производную')
def handle_differentiate_button(message: telebot.types.Message):
    differentiate(message)

@bot.message_handler(func=lambda message: message.text == 'Игра обучение')
def start_game(message: telebot.types.Message):
    user_id = message.from_user.id
    if user_id not in current_game:
        current_game[user_id] = {'score': 0, 'current_question': None}
    send_random_derivative(message)

def send_random_derivative(message):
    user_id = message.from_user.id
    question = random.choice(list(derivatives_table.keys()))
    current_game[user_id]['current_question'] = question
    bot.send_message(user_id, f"Найдите производную: {question}", reply_markup=nav.stopMenu)
    msg = bot.send_message(user_id, "Введите ответ или напишите 'стоп' для завершения игры:")
    bot.register_next_step_handler(msg, check_answer)

def check_answer(message: telebot.types.Message):
    user_id = message.from_user.id
    if message.text.lower() == 'стоп':
        bot.send_message(user_id, f"Игра окончена. Ваш счет: {current_game[user_id]['score']}", reply_markup=nav.mainMenu)
        del current_game[user_id]
        return

    answer = message.text
    question = current_game[user_id]['current_question']
    correct_answer = derivatives_table[question]
    if answer == correct_answer:
        current_game[user_id]['score'] += 1
        bot.send_message(user_id, "Правильно!")
    else:
        bot.send_message(user_id, f"Неправильно. Правильный ответ: {correct_answer}")
    send_random_derivative(message)

if __name__ == "__main__":
    bot.polling()
