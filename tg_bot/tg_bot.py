import telebot
from telebot import types
from db.db_helper import DataBase
import requests
from environment_context import *

bot = telebot.TeleBot('8163739293:AAG4UXBPbzJlOWCxK2gHr1GclYGkZFHtYZY')


def split_long_text(text: str, max_length: int = 4000):
    if len(text) <= max_length:
        return [text]
    parts = []
    while text:
        part = text[:max_length]
        parts.append(part)
        text = text[max_length:]
    return parts


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_consult = types.KeyboardButton('/ai_assistant')
    btn_article = types.KeyboardButton('/article')
    btn_help = types.KeyboardButton('/help')

    markup.add(btn_consult, btn_article, btn_help)

    bot.send_message(
        message.chat.id,
        WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(
        message.chat.id,
        HELP_TEXT,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


@bot.message_handler(commands=['article'])
def ask_article_number(message):
    bot.send_message(
        message.chat.id,
        "Введите номер статьи (1, 2, 3.1):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, process_article_number)


def process_article_number(message):
    try:
        db = DataBase()
        article_number = message.text.strip()
        article_info = db.get_article(article_number=article_number)

        if article_info:
            text_parts = split_long_text(article_info)
            bot.send_message(message.chat.id, text_parts[0], parse_mode="Markdown")
            if len(text_parts) > 1:
                for part in text_parts[1:]:
                    bot.send_message(message.chat.id, part, parse_mode="Markdown")
        else:
            bot.send_message(
                message.chat.id,
                "Статьи с таким номером нет. Попробуйте еще раз (/article)."
            )
    except ValueError:  # Если ввели не число
        bot.send_message(
            message.chat.id,
            "Нужно ввести **число** или номер с пунктом (например, 1 или 1.1). Попробуйте снова (/article).",
            parse_mode="Markdown"
        )


@bot.message_handler(commands=['ai_assistant'])
def start_ai_assistant(message):
    msg = bot.send_message(
        message.chat.id,
        "*Задайте ваш вопрос AI-ассистенту:*\n"
        "(Я отвечу в течение 10-30 секунд)",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, process_ai_request)


def process_ai_request(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json={
                "model": DEFAULT_MODEL,
                "messages": [
                    {"role": "system", "content": LEGAL_CONTEXT["system_prompt"]},
                    *LEGAL_CONTEXT["examples"],
                    {"role": "user", "content": message.text}
                ],
                "temperature": 0.4
            }
        )

        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            safe_text = clean_markdown(ai_response)
            for chunk in split_text(safe_text, 4000):
                bot.send_message(
                    message.chat.id,
                    chunk,
                    parse_mode=None
                )
        else:
            bot.send_message(
                message.chat.id,
                f"❌ Ошибка API (код {response.status_code})"
            )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Произошла ошибка: {str(e)}\nПопробуйте позже или измените запрос."
        )


def clean_markdown(text):
    chars_to_escape = ['*', '_', '[', ']', '`']
    for char in chars_to_escape:
        text = text.replace(char, '')
    return text


def split_text(text, max_len):
    return [text[i:i + max_len] for i in range(0, len(text), max_len)]


bot.infinity_polling()
