import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
Application, CommandHandler, MessageHandler,
CallbackQueryHandler, ConversationHandler,
filters, ContextTypes
)
BOT_TOKEN = "VSTAVЬ_SVOY_TOKEN"
SERVIS = {
"nazvanie": "AvtoMaster",
"adres": "ul. Mekhanizatorov, 12",
"telefon": "+7 (391) 555-12-34",
"rezhim": "Pn-Pt: 8:00-20:00\nSb: 9:00-18:00\nVs: vykhodnoy",
"karta": "https://yandex.ru/maps",
"gis": "https://2gis.ru",
"admin_id": None,
}
USLUGI = [
("Zamena masla i filtrov", "ot 800 rub"),
("Diagnostika dvigatelya", "ot 500 rub"),
("Remont tormoznoy sistemy", "ot 1500 rub"),
("Razval-skhozhdenie", "ot 1200 rub"),
("Shinomontazh", "ot 400 rub/koleso"),
("TO (tekhobsluzhivanie)", "ot 3000 rub"),
("Kuzovnoy remont", "po dogovorennosti"),
("Zamena lamp", "ot 300 rub"),
]
FAQ = [
("Skolko stoit diagnostika?", "ot 500 rub. Pri remonte u nas — BESPLATNO!"),
("Kak dolgo zhdat?", "Bolshinstvo rabot — den v den."),
("Est li garantiya?", "Na vse raboty — 6 mesyatsev."),
("Rabotaete s inomarkami?", "Da! Toyota, BMW, Mercedes, Kia, VAZ i drugie."),
("Nuzhna li zapis zaranee?", "Zhelatelno, no prinimaem i bez zapisi."),
]
AKTSII = [
"Diagnostika BESPLATNO pri remonte ot 2000 rub",
"Shinomontazh 4 kolesa — skidka 15% pri zapisi cherez bota",
"TO pod klyuch — skidka 500 rub dlya novykh klientov",
"Razval-skhozhdenie — vtoroy raz besplatno v techenie mesyatsa",
]
MENU = ReplyKeyboardMarkup([
[" Zapisatsya na remont", " Uslugi i tseny"],
[" Chastye voprosy", " Kontakty i adres"],
[" Otzyvy", " Aktsii i skidki"],
], resize_keyboard=True)
KNOPKA_MENU = ReplyKeyboardMarkup([[" Glavnoe menyu"]], resize_keyboard=True)
IMYa, AVTO, DATA, PROBLEMA = range(4)
logging.basicConfig(level=logging.INFO)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
imya = update.effective_user.first_name
await update.message.reply_text(
"Privet, " + imya + "!\n\n"
"Dobro pozhalovat v " + SERVIS["nazvanie"] + "\n\n"
"Rezhim raboty:\n" + SERVIS["rezhim"] + "\n\n"
"Telefon: " + SERVIS["telefon"] + "\n\n"
"Vyberite nuzhniy razdel:",
reply_markup=MENU
)
async def uslugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
tekst = "Uslugi " + SERVIS["nazvanie"] + ":\n\n"
for nazvanie, tsena in USLUGI:
tekst += "• " + nazvanie + " — " + tsena + "\n"
tekst += "\nZapishites onlayn — bez ocheredi!"
knopki = InlineKeyboardMarkup([[InlineKeyboardButton(" Zapisatsya", callback_data="zapis")]])
await update.message.reply_text(tekst, reply_markup=knopki)
async def voprosy(update: Update, context: ContextTypes.DEFAULT_TYPE):
knopki = [[InlineKeyboardButton(q, callback_data="faq_" + str(i))] for i, (q, _) in enumerate(await update.message.reply_text("Chastye voprosy — vyberite:", reply_markup=InlineKeyboardMarkup(async def fak_otvet(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
i = int(q.data.split("_")[1])
vopros, otvet = FAQ[i]
knopki = InlineKeyboardMarkup([
[InlineKeyboardButton("Nazad", callback_data="faq_back")],
[InlineKeyboardButton(" Zapisatsya", callback_data="zapis")],
])
await q.edit_message_text(vopros + "\n\n" + otvet, reply_markup=knopki)
async def fak_nazad(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
knopki = [[InlineKeyboardButton(v, callback_data="faq_" + str(i))] for i, (v, _) in enumerate(await q.edit_message_text("Chastye voprosy — vyberite:", reply_markup=InlineKeyboardMarkup(async def kontakty(update: Update, context: ContextTypes.DEFAULT_TYPE):
tekst = (
SERVIS["nazvanie"] + "\n\n"
"Adres: " + SERVIS["adres"] + "\n"
"Telefon: " + SERVIS["telefon"] + "\n"
"Rezhim raboty:\n" + SERVIS["rezhim"]
)
knopki = InlineKeyboardMarkup([
[InlineKeyboardButton("Yandeks.Karty", url=SERVIS["karta"])],
[InlineKeyboardButton("2GIS", url=SERVIS["gis"])],
[InlineKeyboardButton(" Zapisatsya", callback_data="zapis")],
])
await update.message.reply_text(tekst, reply_markup=knopki)
async def aktsii(update: Update, context: ContextTypes.DEFAULT_TYPE):
tekst = "Aktsii etogo mesyatsa:\n\n"
for a in AKTSII:
tekst += "• " + a + "\n"
tekst += "\nAktsii do kontsa mesyatsa!"
knopki = InlineKeyboardMarkup([[InlineKeyboardButton(" Zapisatsya so skidkoy", callback_await update.message.reply_text(tekst, reply_markup=knopki)
async def otzyvy(update: Update, context: ContextTypes.DEFAULT_TYPE):
knopki = InlineKeyboardMarkup([[
InlineKeyboardButton("1", callback_data="r_1"),
InlineKeyboardButton("2", callback_data="r_2"),
InlineKeyboardButton("3", callback_data="r_3"),
InlineKeyboardButton("4", callback_data="r_4"),
InlineKeyboardButton("5", callback_data="r_5"),
]])
await update.message.reply_text("Otsenite nash servis ot 1 do 5:", reply_markup=knopki)
async def otziv_otsenka(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
otsenka = int(q.data.split("_")[1])
zvezdy = " " * otsenka
soobshcheniya = {
1: "Nam zhal! Napishite chto poshlo ne tak.",
2: "Spasibo za chestnost. Budem luchshe!",
3: "Spasibo! Rabotaem nad uluchsheniem.",
4: "Otlichno! Rady chto ponravilos.",
5: "Ogromnoe spasibo! Vy nash lyubimiy klient!",
}
knopki = None
if otsenka >= 4:
knopki = InlineKeyboardMarkup([[InlineKeyboardButton("Ostavit otzyv v 2GIS", url=SERVIS["await q.edit_message_text("Vasha otsenka: " + zvezdy + "\n\n" + soobshcheniya[otsenka], reply_async def zapis_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
await update.message.reply_text(" Zapis na remont\n\nShag 1 iz 4\n\nVvedite vashe imya:", return IMYa
async def zapis_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
context.user_data.clear()
await q.message.reply_text(" Zapis na remont\n\nShag 1 iz 4\n\nVvedite vashe imya:", reply_return IMYa
async def shag_imya(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == " Glavnoe menyu":
return await vyhod_v_menyu(update, context)
context.user_data["imya"] = update.message.text
await update.message.reply_text("Shag 2 iz 4\n\nMarka i god avtomobilya:\nPrimer: Toyota return AVTO
async def shag_avto(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == " Glavnoe menyu":
return await vyhod_v_menyu(update, context)
context.user_data["avto"] = update.message.text
await update.message.reply_text(
"Shag 3 iz 4\n\nKogda udobno priekhat?",
reply_markup=ReplyKeyboardMarkup([
["Segodnya", "Zavtra"],
["Poslezavtra", " Glavnoe menyu"],
], resize_keyboard=True)
)
return DATA
async def shag_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == " Glavnoe menyu":
return await vyhod_v_menyu(update, context)
context.user_data["data"] = update.message.text
await update.message.reply_text("Shag 4 iz 4\n\nOpishite problemu:\nPrimer: zamena masla, return PROBLEMA
async def shag_problema(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.text == " Glavnoe menyu":
return await vyhod_v_menyu(update, context)
context.user_data["problema"] = update.message.text
d = context.user_data
user = update.effective_user
await update.message.reply_text(
" Zayavka prinyata!\n\n"
"Imya: " + d["imya"] + "\n"
"Avtomobil: " + d["avto"] + "\n"
"Data: " + d["data"] + "\n"
"Problema: " + d["problema"] + "\n\n"
"Master svyazhetsya s vami v techenie 15 minut.\n"
"Telefon: " + SERVIS["telefon"],
reply_markup=MENU
)
if SERVIS["admin_id"]:
await context.bot.send_message(
SERVIS["admin_id"],
"NOVAYA ZAYaVKA!\n\nImya: " + d["imya"] + "\nAvto: " + d["avto"] + "\nData: " + d[")
context.user_data.clear()
return ConversationHandler.END
async def vyhod_v_menyu(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
await update.message.reply_text("Glavnoe menyu:", reply_markup=MENU)
return ConversationHandler.END
async def tekst(update: Update, context: ContextTypes.DEFAULT_TYPE):
obrabotchiki = {
" Uslugi i tseny": uslugi,
" Chastye voprosy": voprosy,
" Kontakty i adres": kontakty,
" Otzyvy": otzyvy,
" Aktsii i skidki": aktsii,
" Glavnoe menyu": vyhod_v_menyu,
}
fn = obrabotchiki.get(update.message.text)
if fn:
await fn(update, context)
else:
await update.message.reply_text("Vyberite razdel:", reply_markup=MENU)
def main():
app = Application.builder().token(BOT_TOKEN).build()
dialog = ConversationHandler(
entry_points=[
MessageHandler(filters.Regex("^ Zapisatsya na remont$"), zapis_start),
CallbackQueryHandler(zapis_callback, pattern="^zapis$"),
],
states={
IMYa: [MessageHandler(filters.TEXT & ~filters.COMMAND, shag_imya)],
AVTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, shag_avto)],
DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, shag_data)],
PROBLEMA:[MessageHandler(filters.TEXT & ~filters.COMMAND, shag_problema)],
},
fallbacks=[
CommandHandler("start", start),
MessageHandler(filters.Regex("^ Glavnoe menyu$"), vyhod_v_menyu),
],
allow_reentry=True,
)
app.add_handler(CommandHandler("start", start))
app.add_handler(dialog)
app.add_handler(CallbackQueryHandler(fak_otvet, pattern="^faq_\\d+$"))
app.add_handler(CallbackQueryHandler(fak_nazad, pattern="^faq_back$"))
app.add_handler(CallbackQueryHandler(otziv_otsenka, pattern="^r_\\d$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tekst))
print("Bot zapushchen!")
app.run_polling()
if __name__ == "__main__":
main()
