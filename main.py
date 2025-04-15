import telebot
from telebot import types
import os
from datetime import datetime
Token= ''
bot = telebot.TeleBot(Token)

PHOTOS_DIR = 'uploaded_photos'
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_keyboard.add(
    types.KeyboardButton("Загрузить фото"),
    types.KeyboardButton("Помощь"),
    types.KeyboardButton("Start")
)
@bot.message_handler(commands=['start'])
def start_bot(message):
    instructions = f"""Привет, {message.from_user.first_name}!
Это бот для распознавания математических формул.
1. Нажмите кнопку "Загрузить фото"
2. Отправьте фото с математической формулой
3. Получите результат в формате LaTeX """

    bot.send_message(message.chat.id, instructions, reply_markup=main_keyboard)

@bot.message_handler(func=lambda m: m.text == "Start")
def handle_start_button(message):
    start_bot(message)


@bot.message_handler(func=lambda m: m.text == "Помощь")
def help_command(message):
    help_text = """Помощь 

Поддерживаемые форматы:
 - JPG/PNG
  
Если формула не распознается:
1. Проверьте освещение
2. Убедитесь, что формула четкая
3. Попробуйте сделать новое фото

Для начала работы нажмите 'Загрузить фото'"""

    bot.send_message(message.chat.id, help_text, reply_markup=main_keyboard)

@bot.message_handler(func=lambda m: m.text == "Загрузить фото")
def request_photo(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте фото с математической формулой:",
                    reply_markup=types.ReplyKeyboardRemove())

def save_file(file_id, user_id, chat_id):
    try:
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        timenow = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = file_info.file_path.split('.')[-1]
        file_name = f"formula_{timenow}_{user_id}.{file_extension}"
        file_path = os.path.join(PHOTOS_DIR, file_name)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        latex_code = "Здесь будет формула"
        bot.send_message(chat_id, "Фото успешно обработано", reply_markup=main_keyboard)
    except Exception as e:
        error_message = f"Oшибка при обработке фото: {str(e)}"
        bot.send_message(chat_id, error_message)
@bot.message_handler(content_types=['photo'])
def save_photo(message):
    save_file(message.photo[-1].file_id, message.from_user.id, message.chat.id)

@bot.message_handler(content_types=['document'])
def save_document(message):
    if message.document.mime_type in ['image/jpeg', 'image/jpg']:
        save_file(message.document.file_id, message.from_user.id, message.chat.id)
    else:
        bot.reply_to(message, "Пожалуйста, отправляйте только JPG-изображения")


bot.polling(none_stop=True)
