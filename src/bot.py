import telebot
from config import tg_token
from model import get_latex
import cv2
from numpy import frombuffer, uint8

bot = telebot.TeleBot(tg_token)
MAIN_KEYBOARD = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MAIN_KEYBOARD.add(
    telebot.types.KeyboardButton("Распознать формулу"),
    telebot.types.KeyboardButton("Помощь"),
    telebot.types.KeyboardButton("Старт")
)


@bot.message_handler(commands=['start'])
def start_bot(message):
    instructions = (
        f"Добро пожаловать, {message.from_user.first_name}!\n"
        "🤖 Этот бот помогает распознавать математические формулы по фото\n\n"
        "📌 Как использовать:\n"
        "1. Нажмите 'Распознать формулу'\n"
        "2. Отправьте четкое фото формулы\n"
        "3. Получите результат в LaTeX"
    )
    bot.send_message(message.chat.id, instructions, reply_markup=MAIN_KEYBOARD)


@bot.message_handler(func=lambda m: m.text in ["Старт", "Start"])
def handle_start_button(message):
    start_bot(message)


@bot.message_handler(func=lambda m: m.text == "Помощь")
def help_command(message):
    help_text = (
        "🆘 **Помощь**\n\n"
        "✅ **Поддерживаемые форматы:**\n"
        "- JPEG/PNG (качество не ниже 360p)\n\n"
        "🔍 **Если возникают проблемы:**\n"
        "1. Проверьте освещение\n"
        "2. Убедитесь в фокусировке на формуле\n"
        "3. Обрежьте лишние части изображения\n\n"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', reply_markup=MAIN_KEYBOARD)


@bot.message_handler(func=lambda m: m.text == "Распознать формулу")
def request_photo(message):
    bot.send_message(message.chat.id, "📸 Отправьте фото с математической формулой:", reply_markup=telebot.types.ReplyKeyboardRemove())


def process_image(file_id):
    try:
        file_info = bot.get_file(file_id)
        img = cv2.imdecode(frombuffer(bot.download_file(file_info.file_path), dtype=uint8), cv2.IMREAD_GRAYSCALE)
        latex_code = '$' + '$\n$'.join(get_latex(cv2.merge([img, img, img]))) + '$'
        return {'status': 'success', 'result': latex_code}
    except Exception as e:
        return {'status': 'error', 'message': f"Ошибка обработки: {str(e)}"}


def handle(result):
    if result['status'] == 'success':
        response = (
            "✅ Формула успешно распознана!\n\n"
            f"Результат:\n```LaTeX\n{result['result']}\n```"
        )
    else:
        response = f"❌ К сожалению, произошла ошибка, попробуйте еще раз\nДля справки напишите /help"
        print(result['message'])
        f = open('log.txt', 'a+')
        f.write(f"Ошибка: {result['message']}")
        f.close()
    return response


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    result = process_image(message.photo[-1].file_id)
    bot.send_message(message.chat.id, handle(result), parse_mode='Markdown', reply_markup=MAIN_KEYBOARD)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.mime_type in ['image/jpeg', 'image/jpg']:
        result = process_image(message.document.file_id)
        bot.send_message(message.chat.id, handle(result), parse_mode='Markdown', reply_markup=MAIN_KEYBOARD)
    else:
        bot.reply_to(message, "❌ Поддерживаются только изображения в формате JPEG/PNG")


@bot.message_handler(func=lambda message: True)
def handle_document(message):
    bot.send_message(message.chat.id, 'Я тебя не понимаю\nПиши /help', parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['sticker'])
def handle_document(message):
    bot.send_message(message.chat.id, 'Я тебя не понимаю\nПиши /help', parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
