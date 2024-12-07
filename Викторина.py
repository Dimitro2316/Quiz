import telebot
from telebot import types
import random
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


TOKEN = '7867812390:AAH7hP323ZO5Qm4iYp8TX0al9sPS18aW2Y'

bot = telebot.TeleBot(TOKEN)


questions = {
    "Какой самый большой океан?": ["Атлантический", "Индийский", "Тихий", "Северный Ледовитый", "3"],
    "Столица Франции?": ["Берлин", "Лондон", "Париж", "Мадрид", "3"],
    "Сколько планет в Солнечной системе?": ["8", "9", "7", "10", "1"],
    "Самая высокая гора в мире?": ["Мао", "К2", "Эверест", "Лхоцзе", "3"],
}


def get_question():
    question, data = random.choice(list(questions.items()))
    answers = data[:-1]
    correct_answer_index = int(data[-1])
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*answers)
    return question, keyboard, correct_answer_index


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Да")
    msg = bot.send_message(message.chat.id, "Привет! Хотите сыграть в викторине?", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_start_response)


def handle_start_response(message):
    if message.text == "Да":
        question, keyboard, correct_answer_index = get_question()
        msg = bot.send_message(message.chat.id, question, reply_markup=keyboard)
        bot.register_next_step_handler(msg, check_answer, question, correct_answer_index)
    else:
        bot.send_message(message.chat.id, "Хорошо, до скорой встречи!")


def check_answer(message, question, correct_answer_index):
    user_answer = message.text
    correct_answer_index -= 1

    answers = questions[question][:-1]

    try:
        if answers[correct_answer_index] == user_answer:
            bot.send_message(message.chat.id, "Правильно!")
        else:
            bot.send_message(message.chat.id, f"Неправильно. Правильный ответ: "
                                              f"{answers[correct_answer_index]}")
        bot.send_message(message.chat.id, "Хотите ещё один вопрос? Напишите /quiz")
    except (IndexError, TypeError):
        bot.send_message(message.chat.id, "Ошибка обработки ответа. Попробуйте /quiz")


if __name__ == "__main__":
    bot.infinity_polling()


