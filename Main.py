import asyncio
import logging
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = "8849317618:AAHDjXAi_1-q76x0zhq_cyBTQJIwVrIspLA"
YOUR_CHAT_ID = None
TIMEZONE = "Asia/Tashkent"
tz = pytz.timezone(TIMEZONE)

logging.basicConfig(level=logging.INFO)

WEEKLY = {
0:("Dushanba","🛢️ MOYLAR haqida video yoz!"),
1:("Seshanba","🔩 ZAPCHASTLAR haqida video yoz!"),
2:("Chorshanba","❌ MIJOZLAR XATOLARI haqida video yoz!"),
3:("Payshanba","🔧 SERVIS MASLAHATLARI haqida video yoz!"),
4:("Juma","💡 QIZIQARLI FAKT haqida video yoz!"),
5:("Shanba","💰 NARX VA XARAJATLAR haqida video yoz!"),
6:("Yakshanba","🌟 MOTIVATSIYA haqida video yoz!"),
}

async def send_msg(app, text):
    global YOUR_CHAT_ID
    if not YOUR_CHAT_ID:
        try:
            with open("chat_id.txt") as f:
                YOUR_CHAT_ID = int(f.read().strip())
        except:
            return
    await app.bot.send_message(chat_id=YOUR_CHAT_ID, text=text, parse_mode="HTML")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global YOUR_CHAT_ID
    YOUR_CHAT_ID = update.effective_chat.id
    with open("chat_id.txt","w") as f:
        f.write(str(YOUR_CHAT_ID))
    await update.message.reply_html(f"🚗 <b>Avtozapchast Bot ishga tushdi!</b>\n\nHar kuni eslatmalar olasiz!\n\n/bugun /motivatsiya /plan /formula")

async def bugun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    d = datetime.now(tz).weekday()
    kun, mavzu = WEEKLY[d]
    await update.message.reply_html(f"🎬 <b>{kun} — {mavzu}</b>\n\nFormula: HOOK→MUAMMO→YECHIM→CTA")

async def motivatsiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("💪 <b>Bugun ham harakat qil!</b>\n\nKo'p odamlar gapiradi. Sen harakat qilasan. Farq shu! 🔥")

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("📋 <b>Haftalik kontent rejasi:</b>\n\n🛢 Dushanba — Moylar\n🔩 Seshanba — Zapchastlar\n❌ Chorshanba — Mijozlar xatolari\n🔧 Payshanba — Servis maslahatlari\n💡 Juma — Qiziqarli fakt\n💰 Shanba — Narx\n🌟 Yakshanba — Motivatsiya")

async def formula(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("🎬 <b>Video Formula:</b>\n\n⚡ HOOK (3s) — diqqat tort\n❗ MUAMMO (10s) — muammoni ko'rsat\n✅ YECHIM (10s) — yechimni ayt\n📣 CTA (3s) — obuna bo'l")

def setup_scheduler(app):
    s = AsyncIOScheduler(timezone=tz)
    s.add_job(lambda: asyncio.ensure_future(send_msg(app,"🌅 <b>Xayrli tong!</b>\n\n3 ta vazifa:\n1️⃣ Kontent mavzusini tanlash\n2️⃣ 30 daqiqa sport\n3️⃣ Bitta qarorni 24 soat kutib olish\n\n💪 Har kuni 1% yaxshilanish!")), "cron", hour=7, minute=0)
    s.add_job(lambda: asyncio.ensure_future(send_msg(app,f"🎬 Bugungi kontent: {WEEKLY[datetime.now(tz).weekday()][1]}")), "cron", hour=10, minute=0)
    s.add_job(lambda: asyncio.ensure_future(send_msg(app,"💰 <b>Moliya hisobi!</b>\n\nBugun qancha kirdi? Qancha chiqdi?\nDaromadning 10-20% alohida hisobga o'tkaz!")), "cron", hour=18, minute=0)
    s.add_job(lambda: asyncio.ensure_future(send_msg(app,"😤 <b>Asab nazorati!</b>\n\nJahl chiqqanda:\n⏸ 10 soniya kut\n🎯 Muammoga e'tibor qarat\n❓ Foydami yoki hissiyotmi?")), "cron", hour=19, minute=30)
    s.add_job(lambda: asyncio.ensure_future(send_msg(app,"🌙 <b>Kechki tekshiruv</b>\n\n✅ Kontent chiqardingmi?\n✅ Sport qildingmi?\n✅ Asabni boshqardingmi?\n\nErtaga reja yoz!")), "cron", hour=21, minute=0)
    s.start()

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bugun", bugun))
    app.add_handler(CommandHandler("motivatsiya", motivatsiya))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("formula", formula))
    setup_scheduler(app)
    app.run_polling()

if __name__ == "__main__":
    main()
