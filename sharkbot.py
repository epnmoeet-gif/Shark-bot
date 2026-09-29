import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# التوكن والـ ID بتوعك
API_TOKEN = '8619704543:AAE28kaUfCZmiqL6kbPJ_c4nHI7G9qJJYeY'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_ID = 6924901100

# ملف حفظ المستخدمين
USERS_FILE = "users.txt"

# تحميل المستخدمين من الملف إن وجد
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

# حفظ مستخدم جديد في الملف
def save_user(user_id):
    user_ids.add(str(user_id))
    with open(USERS_FILE, "a") as f:
        f.write(f"{user_id}\n")

user_ids = load_users()

# رابط القناة الجديدة
CHANNEL_LINK = "https://t.me/+9Ugw4cPW6RgwMDg8"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # حفظ المستخدم وإرسال إشعار للمدير إذا كان عضواً جديداً
    if str(message.chat.id) not in user_ids:
        save_user(message.chat.id)
        # إشعار دخول عضو جديد 🔔
        try:
            username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد"
            alert_text = (
                f"🔔 **عضو جديد انضم للبوت!**\n\n"
                f"👤 **الاسم:** {message.from_user.first_name}\n"
                f"🆔 **الأيدي:** `{message.chat.id}`\n"
                f"🏷 **اليوزر:** {username}"
            )
            bot.send_message(ADMIN_ID, alert_text, parse_mode='Markdown')
        except:
            pass
    
    user_name = message.from_user.first_name
    
    welcome_message = f"""مرحباً بك {user_name} في بوت الأكواد التراكمية المجانية! 💥
🎯 المكان الوحيد اللي هتاخد منه أكواد مضمونة يوميًا بدون لف ولا دوران

💸 كل يوم كود جديد 🔥
🏆 سحب أسبوعي على جوائز للمشتركين النشطين

⚙️ خطوات الحصول على تراكمي اليوم الـ VIP مجاني:
1️⃣ اضغط بالأسفل على قسيمه اليوم
2️⃣ اشترك في القناة المطلوبة (شرط ضروري ✅)
3️⃣ بعدها هيوصلك كودك فورًا في الرسائل علي الخاص 🎁

⚡ سارع دلوقتي - الأكواد محدودة يوميًا!"""
    
    keyboard = InlineKeyboardMarkup()
    coupon_button = InlineKeyboardButton("🎫 قسيمه اليوم", url=CHANNEL_LINK)
    keyboard.add(coupon_button)
    
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    today_paper_btn = KeyboardButton("✅ ورقة اليوم")
    reply_keyboard.add(today_paper_btn)
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)
    bot.send_message(message.chat.id, "👇 اضغط على الزر بالأسفل للوصول السريع:", reply_markup=reply_keyboard)

@bot.message_handler(func=lambda message: message.text == "✅ ورقة اليوم")
def handle_paper_today(message):
    keyboard = InlineKeyboardMarkup()
    coupon_button = InlineKeyboardButton("🔗 اضغط هنا للانضمام المباشر", url=CHANNEL_LINK)
    keyboard.add(coupon_button)
    
    custom_reply = f"""<b>أهلاً وسهلاً🩵.</b>

<b>تراكمي الخاص بك مجانا 🎁</b>
تم إنشاء رابط الدعوة الخاص بك 👇

اضغط على الرابط بالاسفل ومن ثم طلب الانضمام <i>(القبول فوري ⚡)</i>

<b>Channel:</b>
<b>تراكمي 🔽🔽</b>

{CHANNEL_LINK}"""

    bot.send_message(message.chat.id, custom_reply, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(commands=['broadcast'])
def start_broadcast(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "📢 أرسل الإذاعة الآن (صورة مع نص أو نص فقط):")
        bot.register_next_step_handler(msg, perform_broadcast)
    else:
        bot.reply_to(message, "❌ للمدير فقط!")

def perform_broadcast(message):
    count = 0
    failed = 0
    all_users = list(user_ids)
    
    bot.send_message(message.chat.id, f"📤 جاري الإرسال لـ {len(all_users)} مستخدم...")
    
    for user in all_users:
        try:
            if message.content_type == 'photo':
                bot.send_photo(user, message.photo[-1].file_id, caption=message.caption)
                count += 1
            elif message.content_type == 'text':
                bot.send_message(user, message.text)
                count += 1
            elif message.content_type == 'video':
                bot.send_video(user, message.video.file_id, caption=message.caption)
                count += 1
            elif message.content_type == 'document':
                bot.send_document(user, message.document.file_id, caption=message.caption)
                count += 1
        except Exception as e:
            failed += 1
            continue
            
    bot.send_message(message.chat.id, f"""✅ تم الإرسال بنجاح!
📊 إحصائيات الإرسال:
• تم الإرسال لـ: {count} مستخدم
• فشل الإرسال لـ: {failed} مستخدم
• إجمالي المستخدمين: {len(all_users)}""")

@bot.message_handler(commands=['users'])
def show_users_count(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"👥 عدد المستخدمين الكلي: {len(user_ids)}")
    else:
        bot.reply_to(message, "❌ للمدير فقط!")

if __name__ == "__main__":
    print("✅ البوت يعمل بنجاح...")
    print(f"👤 ADMIN ID: {ADMIN_ID}")
    print(f"📊 عدد المستخدمين المحفوظين: {len(user_ids)}")
    bot.infinity_polling()
