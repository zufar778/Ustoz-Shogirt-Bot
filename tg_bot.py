from telebot import TeleBot, types
from googletrans import Translator
import logging

bot = TeleBot("8441087435:AAEuGF9ahpkaagjBThPnfh5PdQFIUzUpa-0")  
translator = Translator()

@bot.message_handler(commands=["start"])
def startbot(message: types.Message):
    bot.send_message(message.chat.id, "Salom! Men matnni ingliz va o'zbek tillari orasida tarjima qilaman.")

@bot.message_handler(commands=["help"])
def helpbot(message: types.Message):
    bot.send_message(message.chat.id, "Botdan foydalanish uchun /start buyrug'ini yuboring!")

@bot.message_handler(func=lambda message: True)
def translate_text(message: types.Message):
    try:
        original_text = message.text.strip()
        if not original_text:
            bot.send_message(message.chat.id, "Iltimos, tarjima qilish uchun matn yuboring.")
            return

        detected_lang = translator.detect(original_text).lang

        if detected_lang == 'uz':
            translated = translator.translate(original_text, src='uz', dest='en')
        elif detected_lang == 'en':
            translated = translator.translate(original_text, src='en', dest='uz')
        else:
            translated = translator.translate(original_text, dest='uz')

        bot.send_message(message.chat.id, translated.text)

    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("🤖 Bot ishga tushdi...")
    bot.polling(non_stop=True)
