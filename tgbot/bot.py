import os
import platform
import socket
import psutil
import datetime
import requests

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8772262070:AAFgwJTBv8AdUM3y_9f9IjxC6hPvk4gLbrg")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Utility bot online. Use /help")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Commands:
/pcinfo - system info
/iplookup <ip> - ip geolocation
/ping <host> - ping host
/dns <domain> - dns lookup
/time - server time
/uptime - system uptime
""")


async def pcinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    info = f"""
System: {platform.system()}
Release: {platform.release()}
Node: {platform.node()}
CPU: {psutil.cpu_percent()}%
RAM: {psutil.virtual_memory().percent}%
"""

    await update.message.reply_text(info)


async def iplookup(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /iplookup 8.8.8.8")
        return

    ip = context.args[0]

    data = requests.get(f"http://ip-api.com/json/{ip}").json()

    msg = f"""
IP: {ip}
Country: {data.get("country")}
Region: {data.get("regionName")}
City: {data.get("city")}
ISP: {data.get("isp")}
"""

    await update.message.reply_text(msg)


async def dns(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Usage: /dns google.com")
        return

    domain = context.args[0]

    try:
        ip = socket.gethostbyname(domain)
        await update.message.reply_text(f"{domain} → {ip}")
    except:
        await update.message.reply_text("DNS lookup failed")


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(datetime.datetime.now()))


async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    await update.message.reply_text(f"Boot time: {boot}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("pcinfo", pcinfo))
app.add_handler(CommandHandler("iplookup", iplookup))
app.add_handler(CommandHandler("dns", dns))
app.add_handler(CommandHandler("time", time))
app.add_handler(CommandHandler("uptime", uptime))

print("Bot started")
app.run_polling()
