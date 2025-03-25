import telebot
from telebot import types
import os
from datetime import datetime

Token = '7745477532:AAE-x256XxJzdhaZH1ozMnmEa7xc3aI8g48'
bot = telebot.TeleBot(Token)

PHOTOS_DIR = 'uploaded_photos'
if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

@bot.message_handler(commands=['start'])
def start_bot(message):
    instructions = f"""Привет, {message.from_user.first_name}!
Это бот для распознавания математических формул.
1. Нажмите кнопку "Загрузить фото"
2. Отправьте фото с математической формулой
3. Получите результат в формате LaTeX """

    markup = types.InlineKeyboardMarkup()
    button_upload = types.InlineKeyboardButton(text='Загрузить фото', callback_data='upload_photo')
    markup.add(button_upload)
    bot.send_message(message.chat.id, instructions, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'upload_photo')
def handle_upload_photo(call):
    bot.send_message(call.message.chat.id, "Загрузите фото с математической формулой.")

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
        tekst = "Фото успешно сохранено!"
        bot.send_message(chat_id, tekst)
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