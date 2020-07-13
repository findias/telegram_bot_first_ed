import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, 'Напиши своё имя!');
        bot.register_next_step_handler(message, get_name);
    else:
        bot.send_message(message.from_user.id, 'Давай узнаем немножко конфедициальных данных, будет весело. Введи "/reg"')


def get_name(message):
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Напиши  свою фамилию!')
    bot.register_next_step_handler(message, get_surname);


def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    age = message.text
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифирками пожалуйста!');
    question = name + ' ' + surname + ' благодарим за обращение. ' + 'Ваш возраст ' + age + ' лет требованиям удовлетворяет. \nПоздравляю! Кредит оформлен!'
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Подтверждаю!', callback_data='yes');
    keyboard.add(key_yes);
    key_yes_second = types.InlineKeyboardButton(text='Согласен!', callback_data='yes');
    keyboard.add(key_yes_second);
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Спасибо! Ваши данные уже переданы коллекторам. Хорошего дня!');
# RUN
bot.polling(none_stop=True)