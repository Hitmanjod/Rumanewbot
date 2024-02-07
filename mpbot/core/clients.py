import asyncio
import importlib
from datetime import datetime

import pyromod
from pyrogram import Client, idle
from pyrogram.errors import FloodWait

from mpbot.Config import API_HASH, API_ID, BOT_TOKEN, CHAT_ID
from mpbot.plugins import ALL_MODULES

from ..database.all_db import legend_db
from ..database.reedem_db import *
from .logger import LOGS

print(pyromod.listen)


app = Client(
    "Legend",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="mpbot/plugins"),
)


async def check_member():
    ok = user_expiration()
    for user_id, expire in ok.items():
        renew_days = (
            datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S") - datetime.now()
        ).days
        if 2 < renew_days < 3 or 1 > renew_days > 0:
            try:
                await app.send_message(
                    user_id,
                    f"Your subscription is ending in {renew_days} days. Buy a new key if you want to keep using this bot.",
                )
            except:
                pass
        expire_time = datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expire_time:
            await app.kick_chat_member(CHAT_ID, user_id)
            ok.pop(user_id)
    legend_db.set_key("EXPIRATION", ok)


async def Start_MPBot():
    try:
        await app.start()
        await check_member()
        await app.send_message(
            CHAT_ID,
            f"#START\n\n**Version:** - α • 1.2\n**Developed by:** - [Legend](https://t.me/LegendBoy_OP)\n\nYour Market Place Bot Has Been Started Successfully.",
        )
    except FloodWait as e:
        LOGS.error(f"Bot Wants to Sleep For {e.value}")
        await asyncio.sleep(e.value + 5)
    except Exception as f:
        LOGS.error(f)
    for all_module in ALL_MODULES:
        importlib.import_module("mpbot.plugins." + all_module)
        LOGS.info(f"➢ Successfully Imported : {all_module}")
    LOGS.info("==============================")
    LOGS.info("==============================")
    await idle()
