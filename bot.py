from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from datetime import date

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")   # GitHub Secret
ADMIN_ID = 7130966571                # ← မင်း Telegram User ID

VLESS_FILE = "vless.txt"
OUTLINE_FILE = "outline.txt"

VLESS_USERS = "vless_users.txt"
OUTLINE_USERS = "outline_users.txt"
# =========================================


# ---------------- UTILS ------------------
def is_admin(uid: int) -> bool:
    return uid == ADMIN_ID

def today():
    return date.today().isoformat()

def read_lines(file):
    if not os.path.exists(file):
        return []
    with open(file, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]

def write_lines(file, lines):
    with open(file, "w", encoding="utf-8") as f:
        for l in lines:
            f.write(l + "\n")

def clear_file(file):
    open(file, "w").close()
# -----------------------------------------


# ---------------- START ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if is_admin(uid):
        text = (
            "👑 *Admin Panel*\n\n"
            "/addvless <key>\n"
            "/addoutline <key>\n"
            "/clearvless\n"
            "/clearoutline\n"
            "/stats\n\n"
            "👤 User Commands:\n"
            "/getvless\n"
            "/getoutline\n\n"
            "⏳ Limit: 1 key / day"
        )
    else:
        text = (
            "🔐 *Key Bot*\n\n"
            "/getvless\n"
            "/getoutline\n\n"
            "⏳ Limit: 1 key / day"
        )

    await update.message.reply_text(text, parse_mode="Markdown")
# -----------------------------------------


# ---------------- ADMIN ADD ----------------
async def addvless(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        return await update.message.reply_text("Usage: /addvless vless://key")

    with open(VLESS_FILE, "a", encoding="utf-8") as f:
        f.write(" ".join(context.args) + "\n")

    await update.message.reply_text("✅ VLESS key added")


async def addoutline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        return await update.message.reply_text("Usage: /addoutline ss://key")

    with open(OUTLINE_FILE, "a", encoding="utf-8") as f:
        f.write(" ".join(context.args) + "\n")

    await update.message.reply_text("✅ Outline key added")
# ------------------------------------------


# ---------------- CLEAR --------------------
async def clearvless(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    clear_file(VLESS_FILE)
    clear_file(VLESS_USERS)
    await update.message.reply_text("🧹 VLESS keys cleared")


async def clearoutline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    clear_file(OUTLINE_FILE)
    clear_file(OUTLINE_USERS)
    await update.message.reply_text("🧹 Outline keys cleared")
# ------------------------------------------


# ---------------- STATS --------------------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "📊 *Key Stats*\n\n"
        f"🔐 VLESS : {len(read_lines(VLESS_FILE))}\n"
        f"🔑 Outline : {len(read_lines(OUTLINE_FILE))}",
        parse_mode="Markdown"
    )
# ------------------------------------------


# ---------------- USER GET -----------------
async def getvless(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    log = f"{uid}|{today()}"

    users = read_lines(VLESS_USERS)
    if log in users:
        return await update.message.reply_text(
            "⏳ ဒီနေ့ VLESS key ယူပြီးသားပါ\nမနက်ဖြန် ပြန်လာပါ"
        )

    keys = read_lines(VLESS_FILE)
    if not keys:
        return await update.message.reply_text("❌ VLESS key မကျန်တော့ပါ")

    key = keys.pop(0)
    write_lines(VLESS_FILE, keys)

    users.append(log)
    write_lines(VLESS_USERS, users)

    await update.message.reply_text(f"✅ *VLESS Key:*\n\n`{key}`", parse_mode="Markdown")


async def getoutline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    log = f"{uid}|{today()}"

    users = read_lines(OUTLINE_USERS)
    if log in users:
        return await update.message.reply_text(
            "⏳ ဒီနေ့ Outline key ယူပြီးသားပါ\nမနက်ဖြန် ပြန်လာပါ"
        )

    keys = read_lines(OUTLINE_FILE)
    if not keys:
        return await update.message.reply_text("❌ Outline key မကျန်တော့ပါ")

    key = keys.pop(0)
    write_lines(OUTLINE_FILE, keys)

    users.append(log)
    write_lines(OUTLINE_USERS, users)

    await update.message.reply_text(f"✅ *Outline Key:*\n\n`{key}`", parse_mode="Markdown")
# ------------------------------------------


# ================== MAIN ===================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addvless", addvless))
    app.add_handler(CommandHandler("addoutline", addoutline))
    app.add_handler(CommandHandler("clearvless", clearvless))
    app.add_handler(CommandHandler("clearoutline", clearoutline))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("getvless", getvless))
    app.add_handler(CommandHandler("getoutline", getoutline))

    print("🤖 Bot running (Daily limit enabled)")
    app.run_polling()


if __name__ == "__main__":
    main()
