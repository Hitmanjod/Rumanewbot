from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..Config import *
from ..core.clients import app
from ..database.reedem_db import *
from ..helpers.check import check_sudo


@app.on_message(filters.command(["addslot"]))
async def load(bot, msg):
    if not check_sudo(msg.from_user.id):
        return
    editable = await msg.from_user.ask("Send me File")
    x = await editable.download()
    days = await msg.from_user.ask("For 7 days or 30 days?")
    if days.text == "7":
        try:
            with open(x, "r") as f:
                content = f.read()
                new_content = content.split("\n")
                for i in new_content:
                    add_seven_code(i)
            lol = get_seven_code()
            await msg.reply_text(f"Successfully Loaded in 7 days : {len(lol)}")
        except Exception as e:
            return await msg.reply_text(f"ERROR : {e}")
        os.remove(x)
    elif days.text == "30":
        try:
            with open(x, "r") as f:
                content = f.read()
                new_content = content.split("\n")
                for i in new_content:
                    add_monthly_code(i)
            lol = get_monthly_code()
            await msg.reply_text(f"Successfully loaded in 30 days : {len(lol)}")
        except Exception as e:
            return await msg.reply_text(f"Error : {e}")
        os.remove(x)
    else:
        await msg.reply(f"Choose correct days 7 or 30 days \nStart again : /addslot")


@app.on_message(filters.command(["getreedem"]))
async def getered(bot, message):
    if not check_sudo(message.from_user.id):
        return
    sevendays = get_seven_code()
    monthly = get_monthly_code()
    try:
        days = message.text.split(" ")[1]
    except IndexError:
        return await message.reply(
            f"Provide me day 7 and 30 with code, /getreedem 7 or /getreedem 30"
        )
    if days == "7":
        try:
            key_ = sevendays[0]
            await message.reply_text(f"Reedem code for 7 days - `{key_}`")
        except IndexError:
            await message.reply_text("Slot is ended")
    elif days == "30":
        try:
            key_ = monthly[0]
            await message.reply_text(f"Reedem code for 30 days- `{key_}`")
        except IndexError:
            await message.reply_text(
                "There is no slot left add by using command /addslot"
            )


@app.on_message(filters.command(["reedem"]) & ~filters.bot)
async def reedemf(bot, message):
    sevendays = get_seven_code()
    monthly = get_monthly_code()
    ok = user_expiration()
    try:
        code = message.text.split(" ")[1]
    except IndexError:
        await message.reply("Usage format : `/reedem code`")
    user_id = message.from_user.id

    if code in sevendays:
        expiration_time = datetime.now() + timedelta(days=7)
        if user_id in ok:
            days_left = ok[user_id] - datetime.now()
            total_add = days_left + expiration_time
            added = add_expiration(user_id, total)
            now_days = (ok[user_id] - datetime.now()).days
            return await message.reply(f"Plan extended till {now_days}")
        added = add_expiration(user_id, total)
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHAT_ID,
            name="LegendMPBot",
            member_limit=1,
        )
        link = chat_link.invite_link
        await message.reply(
            "Code reedemed successfully! You now have access for 7 days.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Channel Link", url=link)]]
            ),
        )
    elif code in monthly:
        expiration_time = datetime.now() + timedelta(days=30)
        if user_id in ok:
            days_left = ok[user_id] - datetime.now()
            total_add = days_left + expiration_time
            add_expiration(user_id, total)
            now_days = (ok[user_id] - datetime.now()).days
            return await message.reply(f"Plan extended till {now_days}")
        add_expiration(user_id, total)
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHAT_ID,
            name="LegendMPBot",
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
    ok = user_expiration()
    if not user_id in ok:
        return await msg.reply_text(
            "You didnt subscribed my bot Contact owner to subscribe my bot"
        )
    days_left = (ok[user_id] - datetime.now()).days
    await msg.reply_text(f"Days left for your access - {days_left}")
