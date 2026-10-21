import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8638313164:AAEDGTQaGbgVUX8jf_Oxgytz02O4cMsYLA8"
bot = telebot.TeleBot(TOKEN)

# دالة بتلاقي الصورة المرفوعة تلقائياً شو ما كان اسمها
def find_photo():
    for file in os.listdir("."):
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            return file
    return None

@bot.message_handler(commands=['start'])
def send_question(message):
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn1 = InlineKeyboardButton("الكتف", callback_data="correct")
    btn2 = InlineKeyboardButton("التامور", callback_data="wrong")
    btn3 = InlineKeyboardButton("أضلاع", callback_data="wrong")
    btn4 = InlineKeyboardButton("العضلة الدالية", callback_data="wrong")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id, 
        "أهلاً دكتور! جاوب على هالسؤال الطبي البسيط لتفتح المفاجأة 👀:\n\n*اختر الإجابة الصحيحة: ما معنى Scapula؟*", 
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    if call.data == "correct":
        bot.answer_callback_query(call.id, "برافو دكتور! 🎉")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="إجابة صحيحة دكتور! 🎉"
        )
        
        greeting_text = "Surprise it’s Deema!! Happy birthday to the best doctor .I wish you a happy life filled with achievements."
        
        photo_file = find_photo()
        if photo_file:
            with open(photo_file, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=greeting_text)
        else:
            bot.send_message(call.message.chat.id, greeting_text)
            
    else:
        bot.answer_callback_query(call.id, "جواب غلط دكتور! ركز وجرب مرة تانية 😂", show_alert=True)

print("Bot is running...")
bot.infinity_polling()
