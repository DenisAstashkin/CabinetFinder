import telebot
from telebot import types
from graph import *
from key_value_table import get_from_idTable
from media_storage import get_file
from config import BOT_TOKEN, PANORAMA_IMAGE_BUCKET, PANNELUM_URL, PANNELUM_PORT

bot = telebot.TeleBot('8019413008:AAHBCfXzc3xmrkFuabsFSLJSxforsILkjlA')

buttons_main = [
    "🔎 Найти дорогу",
    "ℹ️ Инструкция"
    
]

points = {}

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in buttons_main:
    markup.add(types.KeyboardButton(button))

@bot.message_handler(func=lambda message: message.text == "🔎 Найти дорогу")
def search(message):
    if message.chat.id in points:
        del points[message.chat.id]
    bot.send_message(message.chat.id, "✅ Около какого кабинета Вы находитесь ?", reply_markup=markup)
    bot.register_next_step_handler(message, get_start)

def get_start(message):
    points[message.chat.id] = {'start': message.text}
    bot.send_message(message.chat.id, "💯 В какой кабинеты Вы хотите попасть ?", reply_markup=markup)
    bot.register_next_step_handler(message, get_end)

def get_end(message):
    points[message.chat.id]['end'] = message.text
    try:
        nodes = get_path_between_nodes(get_from_idTable(points[message.chat.id]['start']), get_from_idTable(points[message.chat.id]['end']))
        bot.send_message(message.from_user.id, "Путь:", reply_markup=markup)
    except:
        print("Cannot return the path")
        bot.send_message(message.from_user.id, "Ошибка(Code 562). Некорректные id или пути не существует", reply_markup=markup)
        if message.chat.id in points:
            del points[message.chat.id]
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
    if message.chat.id in points:
        del points[message.chat.id]

@bot.message_handler(func=lambda message: message.text == "ℹ️ Инструкция")
def docs(message):
    logo = open('./assets/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo=logo, caption='Привет! Я бот, который поможет найти тебе <strong>дорогу к аудитории!</strong>\nДавай помогу разобраться.', parse_mode='HTML')
    bot.send_message(message.chat.id, f'У Вас на экране есть две кнопки:\n\n<strong>{buttons_main[0]}</strong> ⬅️ Соответсвенно используется для построения маршрута, но об это попозже.\n\n<strong>{buttons_main[1]}</strong> ⬅️ Используется для того, чтобы напомнить Вам, как пользоваться ботом. Также здесь будет показываться новый функционал бота.', parse_mode='HTML')
    bot.send_message(message.chat.id, f'<strong>{buttons_main[0]}</strong>\nПосле нажатия на кнопку бот запросит аудиторию, около которой Вы находитесь.\n\nВы должны отправить <strong>НОМЕР АУДИТОРИИ / ЛЕСТНИЦУ</strong> рядом с которой Вы стоите.\n\nЗатем бот попросит аудиторию, в которую Вы хотите попасть.\n\nВы должны отправить <strong>НОМЕР</strong> аудиториии, в которую хотите попасть.\n\n🗺 Затем бот вышлет Вам путь, который поможет Вам добраться до нужной Вам аудитории.', parse_mode='HTML')
    
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я бот, который проводит тебя до кабинета!", reply_markup=markup)
    docs(message)
    
@bot.message_handler(commands=['help'])
def start(message):
    docs(message)

bot.polling(none_stop=True, interval=0)