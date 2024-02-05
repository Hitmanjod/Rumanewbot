import asyncio
import importlib
from datetime import datetime

import pyromod
from pyrogram import Client, idle
from pyrogram.errors import FloodWait

from mpbot.Config import API_HASH, API_ID, BOT_TOKEN
from mpbot.plugins import ALL_MODULES
from ..database.reedem_db import *
from .logger import LOGS

print(pyromod.listen)


app = Client(
    "app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="mpbot/plugins"),
)


def check_member():
    ok = user_expiration()
    for user_id, expire in ok.items():
        # expire_time = datetime.strptime(ok[user_id], "%Y-%m-%d %H:%M:%S") - datetime.now()
        # king = expire_time
        print(type(expire))
        if datetime.now() > expire:
            ok.pop(user_id)


async def Start_MPBot():
    try:
        await app.start()
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
