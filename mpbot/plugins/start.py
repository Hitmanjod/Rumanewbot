from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup

from mpbot.Config import MP_LINK

# Start Message


@Client.on_message(filters.command(["start"]) & ~filters.bot)
async def start(bot, msg):
    await msg.reply(
        "Click the button below to join the connected marketplace with this bot",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Marketplace", url=f"{MP_LINK}"),
                    InlineKeyboardButton("About", callback_data="about"),
                ],
                [
                    InlineKeyboardButton("Developers", callback_data="developer"),
                ],
            ]
        ),
    )
