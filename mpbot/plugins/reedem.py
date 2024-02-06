import random
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..Config import *
from ..core.clients import app
from ..database.reedem_db import *
from ..helpers.check import check_sudo


@app.on_message(filters.command(["addslot"]))
async def load(bot, msg):
    if not check_sudo(msg.from_user.id):
        return
    days = await msg.from_user.ask("For `7` days or `30` days?")
    if days.text == "7":
        owo = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        a = owo.split(" ")
        for _ in range(20):
            code = ""
            for _ in range(4):
                code += random.choice(a)
            code = f"{code[0]}{code[1]}{code[2]}{code[3]}-{random.choice(a)}{random.choice(a)}{random.choice(a)}-{random.choice(a)}{random.choice(a)}{random.choice(a)}"
            add_seven_code(code)
        owo = get_seven_code()
        await msg.reply(
            f"Total Loaded Slot in My Bot for 7 days : {len(owo)}\n\nCheck Reedem Code By Using /getreedem"
        )
    elif days.text == "30":
        owo = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        a = owo.split(" ")
        for _ in range(20):
            code = ""
            for _ in range(4):
                code += random.choice(a)
            code = f"{code[0]}{code[1]}{code[2]}{code[3]}-{random.choice(a)}{random.choice(a)}{random.choice(a)}-{random.choice(a)}{random.choice(a)}{random.choice(a)}"
            add_monthly_code(code)
        owo = get_monthly_code()
        await msg.reply_text(
            f"Total Loaded Slot in My Bot for 30 days : {len(owo)}\n\nCheck Reedem Code By Using /getreedem"
        )
    else:
        await msg.reply(f"Choose correct days 7 or 30 days \nStart again : /addslot")


@app.on_message(filters.command(["getreedem"]))
async def getered(bot, message):
    if not check_sudo(message.from_user.id):
        return
    sevendays = get_seven_code()
    monthly = get_monthly_code()
    tsev = "**Reedem code for 7 days**\n"
    ttol = 0
    for _key in sevendays:
        ttol += 1
        tsev += f"{ttol}. `{_key}`\n"
    tsev += "\n\n**Reedem Code For 30 Days**\n"
    for skey in monthly:
        ttol += 1
        tsev += f"{ttol}. `{skey}`\n"
    await message.reply_text(tsev)


@Client.on_message(filters.command(["reedem"]))
async def reeyydemf(bot, message):
    sevendays = get_seven_code()
    monthly = get_monthly_code()
    ok = user_expiration()
    try:
        code = message.text.split(" ")[1]
    except IndexError:
        return await message.reply("Usage format : `/reedem code`")
    user_id = message.from_user.id
    if code in sevendays:
        expire_time = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        if user_id in ok:
            expire_time = (
                datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S") - datetime.now()
            )
            king = expire_time + timedelta(days=7) + datetime.now()
            string_days = king.strftime("%Y-%m-%d %H:%M:%S")
            add_expiration(user_id, string_days)
            remove_seven_code(code)
            return await message.reply(f"Plan extended till {string_days}")
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHAT_ID,
            name="LegendMPBot",
            member_limit=1,
        )
        link = chat_link.invite_link
        add_expiration(user_id, expire_time)
        remove_seven_code(code)
        await message.reply(
            "Code reedemed successfully! You now have access for 7 days.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Channel Link", url=link)]]
            ),
        )
    elif code in monthly:
        expire_time = (datetime.now() + timedelta(days=30)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        if user_id in ok:
            expire_time = (
                datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S") - datetime.now()
            )
            king = expire_time + timedelta(days=30) + datetime.now()
            string_days = king.strftime("%Y-%m-%d %H:%M:%S")
            add_expiration(user_id, string_days)
            remove_monthly_code(code)
            return await message.reply(f"Plan extended till {string_days}")
        chat_link = await bot.create_chat_invite_link(
            chat_id=CHAT_ID,
            name="LegendMPBot",
            member_limit=1,
        )
        link = chat_link.invite_link
        add_expiration(user_id, expire_time)
        remove_monthly_code(code)
        await message.reply(
            "Code reedemed successfully! You now have access for 30 days.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Channel Link", url=link)]]
            ),
        )
    else:
        return await message.reply_text(f"Invalid Reedem Code")


@app.on_message(filters.command(["sub"]) & ~filters.bot)
async def subhh(bot, msg):
    user_id = msg.from_user.id
    ok = user_expiration()
    if not user_id in ok:
        return await msg.reply_text(
            "You didnt subscribed my bot Contact owner to subscribe my bot"
        )
    days_left = (
        datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S") - datetime.now()
    ).days
    await msg.reply_text(f"You have {days_left} days left on your subscription!")
