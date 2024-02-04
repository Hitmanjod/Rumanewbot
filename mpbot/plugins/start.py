import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from drop.database.storefile_db import *
from drop.database.time_db import *
from mpbot.Config import MP_LINK
from drop.helpers.check import check_sudo

# Start Message

@Client.on_message(filters.command(["start"]) & ~filters.bot)
async def start(bot, msg):
    await msg.reply("Click the button below to join the connected marketplace with this bot",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Marketplace", url=f"{MP_LINK}"),
                                InlineKeyboardButton("About", callback_data="about"),
                            ],
                            [
                                InlineKeyboardButton("Developers", callback_data="developer"),
                            ]
                        ]
                    )
                   )





