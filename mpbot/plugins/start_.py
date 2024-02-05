from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from mpbot.Config import MP_LINK

from ..core.clients import app

# Start Message


@app.on_message(filters.command(["start"]) & ~filters.bot)
async def staaart(bot, msg):
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
    await query.edit_message_text("Processing...")
    user_id = "Stats Of MarketPlace\n\n"
    ok = user_expiration()
    for user_id, expire in ok.items():
        peer_idsolve = await app.resolve_peer(user_id)
        user = await bot.get_users(peer_idsolve)
        name = user.first_name
        user_id += f"• {name} : {expire}"
    await query.edit_message_text(user_id)


@app.on_callback_query(filters.regex("developer"))
async def dveke(_, query: CallbackQuery):
    user_id = """
    I am a skilled Coder, serving over 100 clients monthly with swift turnaround times. Specializing in Custom Bot creation, I exclusively accept cryptocurrency payments.
    **Developer** : [Legend](https://t.me/LegendBoy_OP)
    """
    await query.edit_message_text(user_id)


@app.on_callback_query(filters.regex("about"))
async def abouts(_, query: CallbackQuery):
    user_id = """
Description : This telegram bot can be used for your marketplace or any other work.
✔️Functions : By this bot you can add special users in a private group and everything which they will post inside the private group will be forwarded inside the linked channel.
✔️ Commands :
/sub : Check Posts Left / day.
/redeem : Redeem key to get post bot access.
/start : Check whether bot is alive or not.
    """
    await query.edit_message_text(user_id)
