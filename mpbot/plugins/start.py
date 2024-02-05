from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mpbot.Config import MP_LINK

from ..core.clients import app

# Start Message


@Client.on_message(filters.command(["start"]) & ~filters.bot)
async def start(bot, msg):
    await msg.reply(
        "Click the button below to join the connected marketplace with this bot",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Marketplace", url=f"{MP_LINK}"),
                    InlineKeyboardButton("Stats", callback_data="stats"),
                ],
                [
                    InlineKeyboardButton("Developers", callback_data="developer"),
                    InlineKeyboardButton("About", callback_data="about"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("stats"))
async def stats(_, query: CallbackQuery):
    user_id = "Stats Of MarketPlace"
    await query.edit_message_text(user_id)


@app.on_callback_query(filters.regex("developer"))
async def stats(_, query: CallbackQuery):
    user_id = "Developer"
    await query.edit_message_text(user_id)


@app.on_callback_query(filters.regex("about"))
async def stats(_, query: CallbackQuery):
    user_id = "About"
    await query.edit_message_text(user_id)
