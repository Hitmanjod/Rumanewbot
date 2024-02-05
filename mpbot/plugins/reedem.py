from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..Config import *
from ..core.clients import app

sevendays = ["afff", "afds"]
monthly = ["ada", "afddf"]

user_access_expiration = {}


@app.on_message(filters.command(["getreedem"]) & ~filters.bot)
async def getered(bot, message):
    days = message.text.split(" ")[1]
    if days == "7":
        try:
            sevendays[0]
            await message.reply_text(f"Reedem code for 7 days - `{key_}`")
        except IndexError:
            await message.reply_text(
                "Reedem code is ended for 7 days. Add more renew code by using command /load"
            )
    elif days == "30":
        try:
            monthly[0]
            await message.reply_text(f"Reedem code for 30 days- `{key_}`")
        except IndexError:
            await message.reply_text(
                "Reedem code is ended for monthly. Add more code by using command /load"
            )


@app.on_message(filters.command(["reedem"]) & ~filters.bot)
async def reedemf(bot, message):
    try:
        code = message.text.split(" ")[1]
    except IndexError:
        await message.reply("/reedem code")
    user_id = message.from_user.id
    if code in sevendays:
        expiration_time = datetime.now() + timedelta(days=7)
        user_access_expiration[user_id] = expiration_time
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            name="LegendBotMPBot",
            member_limit=1,
        )
        link = chat_link.invite_link
        await message.reply(
            "Code reedemed successfully! You now have access for 7 days.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Channel Link", url=link)]]
            ),
        )
        sevendays.remove(code)
    elif code in monthly:
        expiration_time = datetime.now() + timedelta(days=30)
        user_access_expiration[user_id] = expiration_time
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            name="LegendBotMPBot",
            member_limit=1,
        )
        link = chat_link.invite_link
        await message.reply(
            "Code reedemed successfully! You now have access for 30 days.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Channel Link", url=link)]]
            ),
        )
        monthly.remove(code)
    else:
        await message.reply_text(f"Invalid Code")


@app.on_message(filters.command(["sub"]) & ~filters.bot)
async def subhh(bot, msg):
    user_id = msg.from_user.id
    if not user_id in user_access_expiration:
        return await msg.reply_text(
            "You didnt subscribed my bot Contact owner to subscribe my bot"
        )
    days_left = (user_access_expiration[user_id] - datetime.now()).days
    await msg.reply_text(f"Days left for your access - {days_left}")
