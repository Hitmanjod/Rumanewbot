from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from datetime import datetime, timedelta
from mpbot.Config import MP_LINK

from ..core.clients import app

sevendays = ["afff", "afds"]
monthly = ["ada", "afddf"]

user_access_expiration = {}

@app.on_message(filters.command(["reedem"]) & ~filters.bot)
async def start(bot, msg):
    code = message.text.split(" ")[1]
    user_id = message.from_user.id
    if code in sevendays:
        expiration_time = datetime.now() + timedelta(days=7)
        user_access_expiration[user_id] = expiration_time
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            name="LegendBotMPBot",
            limit=1,
        )
        link = chat_link.invite_link
        await message.reply(
            "Code reedemed successfully! You now have access for 7 days.", 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Channel Link", url=link)
                    ]
                ]
            )
        )
        sevendays.remove(code)
    elif code in monthly:
        expiration_time = datetime.now() + timedelta(days=30)
        user_access_expiration[user_id] = expiration_time
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            name="LegendBotMPBot",
            limit=1,
        )
        link = chat_link.invite_link
        await message.reply(
            "Code reedemed successfully! You now have access for 30 days.", 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Channel Link", url=link)
                    ]
                ]
            )
        )
        monthly.remove(code)
    else:
        await message.reply_text(f"Invalid Code")
        

@app.on_message(filters.command(["sub"]) & ~filters.bot)
async def start(bot, msg):
    user_id = msg.from_user.id
    if not user_id in user_access_expiration:
        return await msg.reply_text("You didnt subscribed my bot Contact owner to subscribe my bot")
    days_left = (user_access_expiration[user_id] - datetime.now()).days
    await message.reply_text(f"Days left for your access - {days_left}")
    




