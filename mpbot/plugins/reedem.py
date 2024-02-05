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
    editable = await msg.from_user.ask("Send me File")
    x = await editable.download()
    days = await msg.from_user.ask("For `7` days or `30` days?")
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
            f"Provide me day 7 and 30 with code, `/getreedem 7` or `/getreedem 30`"
        )
    if days == "7":
        try:
            tsev = ""
            ttol = 0
            for _key in sevendays:
                ttol += 1
                tsev += f"Reedem Code {ttol} : `{_key}`\n"
            await message.reply_text(f"Reedem code for 7 days - {tsev}")
        except Exception:
            await message.reply_text(
                "There is no slot left for 7 days add by using command /addslot"
            )
    elif days == "30":
        try:
            tsev = ""
            ttol = 0
            for _key in monthly:
                ttol += 1
                tsev += f"Code {ttol} : {_key}\n"
            await message.reply_text(f"Reedem code for 30 days - `{tsev}`")
        except Exception:
            await message.reply_text(
                "There is no slot left for 30 days add by using command /addslot"
            )


@Client.on_message(filters.command(["reedem"]))
async def reeyydemf(bot, message):
    sevendays = get_seven_code()
    monthly = get_monthly_code()
    ok = user_expiration()
    try:
        code = message.text.split(" ")[1]
    except IndexError:
        await message.reply("Usage format : `/reedem code`")
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
    days_left = datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S") - datetime.now()
    await msg.reply_text(f"Days left for your access - {days_left}")
