import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
Application, CommandHandler, MessageHandler,
CallbackQueryHandler, ConversationHandler,
filters, ContextTypes
)

BOT_TOKEN = “8704554931:AAGY7TCnazi-N7Ud2xAnlEwNwr8ZmBVHvLE”

СЕРВИС = {
“название”: “АвтоМастер”,
“адрес”:    “ул. Механизаторов, 12”,
“телефон”:  “+7 (391) 555-12-34”,
“режим”:    “Пн-Пт: 8:00-20:00\nСб: 9:00-18:00\nВс: выходной”,
“карта”:    “https://yandex.ru/maps”,
“2гис”:     “https://2gis.ru”,
“admin_id”: None,
}

УСЛУГИ = [
(“Замена масла и фильтров”,  “от 800 руб”),
(“Диагностика двигателя”,    “от 500 руб”),
(“Ремонт тормозной системы”, “от 1500 руб”),
(“Развал-схождение”,         “от 1200 руб”),
(“Шиномонтаж”,               “от 400 руб/колесо”),
(“ТО (техобслуживание)”,     “от 3000 руб”),
(“Кузовной ремонт”,          “по договорённости”),
(“Замена ламп”,              “от 300 руб”),
]

FAQ = [
(“Сколько стоит диагностика?”, “от 500 руб. При ремонте у нас — БЕСПЛАТНО!”),
(“Как долго ждать?”,           “Большинство работ — день в день.”),
(“Есть ли гарантия?”,          “На все работы — 6 месяцев.”),
(“Работаете с иномарками?”,    “Да! Toyota, BMW, Mercedes, Kia, ВАЗ и другие.”),
(“Нужна ли запись заранее?”,   “Желательно, но принимаем и без записи.”),
]

АКЦИИ = [
“Диагностика БЕСПЛАТНО при ремонте от 2000 руб”,
“Шиномонтаж 4 колеса — скидка 15% при записи через бота”,
“ТО под ключ — скидка 500 руб для новых клиентов”,
“Развал-схождение — второй раз бесплатно в течение месяца”,
]

МЕНЮ = ReplyKeyboardMarkup([
[“📅 Записаться на ремонт”, “🔧 Услуги и цены”],
[“❓ Частые вопросы”,        “📍 Контакты и адрес”],
[“⭐ Отзывы”,                “🎁 Акции и скидки”],
], resize_keyboard=True)

КНОПКА_МЕНЮ = ReplyKeyboardMarkup([[“🏠 Главное меню”]], resize_keyboard=True)

ИМЯ, АВТО, ДАТА, ПРОБЛЕМА = range(4)

logging.basicConfig(level=logging.INFO)

async def старт(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
имя = update.effective_user.first_name
await update.message.reply_text(
f”Привет, {имя}!\n\n”
f”Добро пожаловать в {СЕРВИС[‘название’]}\n\n”
f”Режим работы:\n{СЕРВИС[‘режим’]}\n\n”
f”Телефон: {СЕРВИС[‘телефон’]}\n\n”
f”Выберите нужный раздел:”,
reply_markup=МЕНЮ
)

async def услуги(update: Update, context: ContextTypes.DEFAULT_TYPE):
текст = f”Услуги {СЕРВИС[‘название’]}:\n\n”
for название, цена in УСЛУГИ:
текст += f”• {название} — {цена}\n”
текст += “\nЗапишитесь онлайн — без очереди!”
кнопки = InlineKeyboardMarkup([[InlineKeyboardButton(“📅 Записаться”, callback_data=“запись”)]])
await update.message.reply_text(текст, reply_markup=кнопки)

async def вопросы(update: Update, context: ContextTypes.DEFAULT_TYPE):
кнопки = [[InlineKeyboardButton(q, callback_data=f”faq_{i}”)] for i, (q, _) in enumerate(FAQ)]
await update.message.reply_text(“Частые вопросы — выберите:”, reply_markup=InlineKeyboardMarkup(кнопки))

async def фак_ответ(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
i = int(q.data.split(”_”)[1])
вопрос, ответ = FAQ[i]
кнопки = InlineKeyboardMarkup([
[InlineKeyboardButton(“Назад”, callback_data=“faq_back”)],
[InlineKeyboardButton(“📅 Записаться”, callback_data=“запись”)],
])
await q.edit_message_text(f”{вопрос}\n\n{ответ}”, reply_markup=кнопки)

async def фак_назад(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
кнопки = [[InlineKeyboardButton(v, callback_data=f”faq_{i}”)] for i, (v, _) in enumerate(FAQ)]
await q.edit_message_text(“Частые вопросы — выберите:”, reply_markup=InlineKeyboardMarkup(кнопки))

async def контакты(update: Update, context: ContextTypes.DEFAULT_TYPE):
текст = (
f”{СЕРВИС[‘название’]}\n\n”
f”Адрес: {СЕРВИС[‘адрес’]}\n”
f”Телефон: {СЕРВИС[‘телефон’]}\n”
f”Режим работы:\n{СЕРВИС[‘режим’]}”
)
кнопки = InlineKeyboardMarkup([
[InlineKeyboardButton(“Яндекс.Карты”, url=СЕРВИС[“карта”])],
[InlineKeyboardButton(“2ГИС”, url=СЕРВИС[“2гис”])],
[InlineKeyboardButton(“📅 Записаться”, callback_data=“запись”)],
])
await update.message.reply_text(текст, reply_markup=кнопки)

async def акции(update: Update, context: ContextTypes.DEFAULT_TYPE):
текст = “Акции этого месяца:\n\n”
for а in АКЦИИ:
текст += f”• {а}\n”
текст += “\nАкции до конца месяца!”
кнопки = InlineKeyboardMarkup([[InlineKeyboardButton(“📅 Записаться со скидкой”, callback_data=“запись”)]])
await update.message.reply_text(текст, reply_markup=кнопки)

async def отзывы(update: Update, context: ContextTypes.DEFAULT_TYPE):
кнопки = InlineKeyboardMarkup([[
InlineKeyboardButton(“1”, callback_data=“r_1”),
InlineKeyboardButton(“2”, callback_data=“r_2”),
InlineKeyboardButton(“3”, callback_data=“r_3”),
InlineKeyboardButton(“4”, callback_data=“r_4”),
InlineKeyboardButton(“5”, callback_data=“r_5”),
]])
await update.message.reply_text(“Оцените наш сервис от 1 до 5:”, reply_markup=кнопки)

async def отзыв_оценка(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
оценка = int(q.data.split(”_”)[1])
звёзды = “⭐” * оценка
сообщения = {
1: “Нам жаль! Напишите что пошло не так.”,
2: “Спасибо за честность. Будем лучше!”,
3: “Спасибо! Работаем над улучшением.”,
4: “Отлично! Рады что понравилось.”,
5: “Огромное спасибо! Вы наш любимый клиент!”,
}
кнопки = None
if оценка >= 4:
кнопки = InlineKeyboardMarkup([[InlineKeyboardButton(“Оставить отзыв в 2ГИС”, url=СЕРВИС[“2гис”])]])
await q.edit_message_text(f”Ваша оценка: {звёзды}\n\n{сообщения[оценка]}”, reply_markup=кнопки)

async def запись_старт(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
await update.message.reply_text(“📅 Запись на ремонт\n\nШаг 1 из 4\n\nВведите ваше имя:”, reply_markup=КНОПКА_МЕНЮ)
return ИМЯ

async def запись_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
context.user_data.clear()
await q.message.reply_text(“📅 Запись на ремонт\n\nШаг 1 из 4\n\nВведите ваше имя:”, reply_markup=КНОПКА_МЕНЮ)
return ИМЯ

async def шаг_имя(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == “🏠 Главное меню”:
return await выход_в_меню(update, context)
context.user_data[“имя”] = update.message.text
await update.message.reply_text(“Шаг 2 из 4\n\nМарка и год автомобиля:\nПример: Toyota Camry 2020”, reply_markup=КНОПКА_МЕНЮ)
return АВТО

async def шаг_авто(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == “🏠 Главное меню”:
return await выход_в_меню(update, context)
context.user_data[“авто”] = update.message.text
await update.message.reply_text(
“Шаг 3 из 4\n\nКогда удобно приехать?”,
reply_markup=ReplyKeyboardMarkup([[“Сегодня”, “Завтра”], [“Послезавтра”, “🏠 Главное меню”]], resize_keyboard=True)
)
return ДАТА

async def шаг_дата(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == “🏠 Главное меню”:
return await выход_в_меню(update, context)
context.user_data[“дата”] = update.message.text
await update.message.reply_text(“Шаг 4 из 4\n\nОпишите проблему:\nПример: замена масла, стук в подвеске”, reply_markup=КНОПКА_МЕНЮ)
return ПРОБЛЕМА

async def шаг_проблема(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == “🏠 Главное меню”:
return await выход_в_меню(update, context)
context.user_data[“проблема”] = update.message.text
д = context.user_data
user = update.effective_user
await update.message.reply_text(
f”✅ Заявка принята!\n\n”
f”Имя: {д[‘имя’]}\n”
f”Автомобиль: {д[‘авто’]}\n”
f”Дата: {д[‘дата’]}\n”
f”Проблема: {д[‘проблема’]}\n\n”
f”Мастер свяжется с вами в течение 15 минут.\n”
f”Телефон: {СЕРВИС[‘телефон’]}”,
reply_markup=МЕНЮ
)
if СЕРВИС[“admin_id”]:
await context.bot.send_message(
СЕРВИС[“admin_id”],
f”НОВАЯ ЗАЯВКА!\n\nИмя: {д[‘имя’]} (@{user.username or ‘нет’})\nАвто: {д[‘авто’]}\nДата: {д[‘дата’]}\nПроблема: {д[‘проблема’]}”
)
context.user_data.clear()
return ConversationHandler.END

async def выход_в_меню(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
await update.message.reply_text(“Главное меню:”, reply_markup=МЕНЮ)
return ConversationHandler.END

async def текст(update: Update, context: ContextTypes.DEFAULT_TYPE):
обработчики = {
“🔧 Услуги и цены”:    услуги,
“❓ Частые вопросы”:    вопросы,
“📍 Контакты и адрес”: контакты,
“⭐ Отзывы”:            отзывы,
“🎁 Акции и скидки”:   акции,
“🏠 Главное меню”:      выход_в_меню,
}
fn = обработчики.get(update.message.text)
if fn:
await fn(update, context)
else:
await update.message.reply_text(“Выберите раздел:”, reply_markup=МЕНЮ)

def main():
app = Application.builder().token(BOT_TOKEN).build()
диалог = ConversationHandler(
entry_points=[
MessageHandler(filters.Regex(”^📅 Записаться на ремонт$”), запись_старт),
CallbackQueryHandler(запись_callback, pattern=”^запись$”),
],
states={
ИМЯ:      [MessageHandler(filters.TEXT & ~filters.COMMAND, шаг_имя)],
АВТО:     [MessageHandler(filters.TEXT & ~filters.COMMAND, шаг_авто)],
ДАТА:     [MessageHandler(filters.TEXT & ~filters.COMMAND, шаг_дата)],
ПРОБЛЕМА: [MessageHandler(filters.TEXT & ~filters.COMMAND, шаг_проблема)],
},
fallbacks=[
CommandHandler(“start”, старт),
MessageHandler(filters.Regex(”^🏠 Главное меню$”), выход_в_меню),
],
allow_reentry=True,
)
app.add_handler(CommandHandler(“start”, старт))
app.add_handler(диалог)
app.add_handler(CallbackQueryHandler(фак_ответ,    pattern=”^faq_\d+$”))
app.add_handler(CallbackQueryHandler(фак_назад,    pattern=”^faq_back$”))
app.add_handler(CallbackQueryHandler(отзыв_оценка, pattern=”^r_\d$”))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, текст))
print(f”Бот запущен!”)
app.run_polling()

if **name** == “**main**”:
main()