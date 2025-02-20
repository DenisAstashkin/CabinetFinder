import telebot
from telebot import types
from graph import *
from key_value_table import get_from_idTable
from media_storage import save_file, get_file
from config import BOT_TOKEN, PANORAMA_IMAGE_BUCKET, PANNELUM_URL, PANNELUM_PORT

bot = telebot.TeleBot(BOT_TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

buttons = [
    "/path"
]

for button in buttons:
    markup.add(types.KeyboardButton(button))
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "👋 Привет! Я бот, который проводит тебя до кабинета!", reply_markup=markup)
    
@bot.message_handler(commands=['path', 'get_path'])
def get_path(message):
    
    bot.send_message(message.from_user.id, "Введите два id через пробел", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def message_input_step(message):
        try:
            text = message.text
            id1 = text.split(" ")[0]
            id2 = text.split(" ")[1]
            nodes = get_path_between_nodes(get_from_idTable(id1), get_from_idTable(id2))
            bot.send_message(message.from_user.id, "Путь:", reply_markup=markup)
        except:
            print("Cannot return the path")
            bot.send_message(message.from_user.id, "Ошибка(Code 562). Некорректные id или пути не существует", reply_markup=markup)
            return

        for node in nodes:
            name = ""
            
            try:
                panorama_image_filename = node._properties["panorama_image"]
            except KeyError:
                panorama_image_filename = "3b6e95e3a1b9f54c7b1367c2e7863e2c.jpg" #default panorama

        

            #panorama_url = "PANNELLUME_SERVICE" + "BUCKET_URL" + panorama_image_filename
            image_url = "google.com" + "/" + PANORAMA_IMAGE_BUCKET + '/' + panorama_image_filename
            panorama_url = PANNELUM_URL + ":" + PANNELUM_PORT + "/src/standalone/pannellum.htm#panorama=" + image_url

            button_foo = types.InlineKeyboardButton('Панорама', callback_data='foo', url = panorama_url)

            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(button_foo)

            try:
                name = node._properties["name"]
            except KeyError:
                pass
            
            local_filename = get_file(node._properties["image"])
            
            bot.send_photo(message.chat.id, photo=open(local_filename, 'rb'), caption=name, reply_markup = keyboard)
        

    bot.register_next_step_handler(message, message_input_step) #добавляем следующий шаг, перенаправляющий пользователя на message_input_step


bot.polling(none_stop=True, interval=0)