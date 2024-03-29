import asyncio
import logging
import time
from logging.handlers import RotatingFileHandler

from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

api_id = 3748059
api_hash = "f8c9df448f3ba20a900bc2ffc8dae9d5"
bot_token = "6928722311:AAErBpeaDLWWZaZIfPGMXxK21P-HPKYH8Oc"
chat_id = -1001957999583
channel_id = -1001803025958
mp_link = "https://t.me/ZoneMP"
allow_id = "5591734243"
max_posts_per_day = 4
max_time = 600

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGS = logging.getLogger()

# =========== Client ===========#

bot = Client(
    "bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
)

last_message_times = {}
user_message_count = {}
allowed_user_id = allow_id.split(" ")


@bot.on_message(filters.command(["start"]) & ~filters.bot)
async def start(bot: Client, message: Message):
    await message.reply(
        "Click the button below to join the #Official Marketplace",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join channel", url=f"{mp_link}")]]
        ),
    )


@bot.on_message(filters.command(["deletelast"]) & ~filters.bot)
async def start(bot: Client, message: Message):
    if str(message.from_user.id) not in str(allowed_user_id):
        return
    contain_id = message.text.split(" ")
    if len(contain_id) == 2:
        lol_message = int(contain_id[1])
        await bot.delete_messages(channel_id, lol_message)
    else:
        msg = await bot.send_message(channel_id, " Deleting Last Message ")
        current_id = msg.id
        await msg.delete()
        last_message = current_id - 1
        try:
            await bot.delete_messages(channel_id, last_message)
        except Exception as e:
            print(e)


@bot.on_message(filters.chat(chat_id) & ~filters.bot)
async def forward(bot: Client, message: Message):
    user_id = message.from_user.id
    global last_message_times, user_message_count
    if message.text == "/sub":
        if message.reply_to_message:
            print(f"Checking sub for {message.reply_to_message.from_user.id}")
            if user_message_count.get(message.reply_to_message.from_user.id, 0) >= int(
                max_posts_per_day
            ):
                remaining_posts = 0
            else:
                remaining_posts = int(max_posts_per_day) - user_message_count.get(
                    message.reply_to_message.from_user.id, 0
                )
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(message.reply_to_message.from_user.id, 0)}"
            return await message.reply_text(remaining_posts_message)
        else:
            if user_message_count.get(user_id, 0) >= int(max_posts_per_day):
                remaining_posts = 0
            else:
                remaining_posts = int(max_posts_per_day) - user_message_count.get(
                    user_id, 0
                )
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(user_id, 0)}"
            return await message.reply_text(remaining_posts_message)
    try:
        if message.text.startswith(".") or message.text.startswith("/"):
            return print("Message Started From . or /")
    except:
        pass
    if user_id in last_message_times:
        if str(user_id) in str(allowed_user_id):
            last_message_times[user_id] = time.time()
        else:
            if user_message_count.get(user_id, 0) >= int(max_posts_per_day):
                return await message.reply_text(
                    "Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit."
                )
            time_since_last_message = time.time() - last_message_times[user_id]
            if time_since_last_message < int(max_time):
                remaining_time = int(max_time) - time_since_last_message
                cooldown_message = f"Please wait {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds before posting another message to the channel.\n\n**Your post is added to queue & will be posted after {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds automatically.**"
                await message.reply_text(cooldown_message)
                await asyncio.sleep(remaining_time)
                if user_message_count.get(user_id, 0) >= int(max_posts_per_day):
                    return await message.reply_text(
                        "Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit."
                    )
                last_message_times[user_id] = time.time()
                if message.text:
                    await bot.send_message(
                        channel_id,
                        f"{message.text.html}\n\nPosted by @{message.from_user.username}",
                    )
                elif message.media:
                    file_id = await bot.download_media(message)
                    await bot.send_photo(
                        channel_id,
                        file_id,
                        caption=f"{message.caption.html}\n\nPosted by @{message.from_user.username}",
                    )
                else:
                    return print("This is document")
                user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
                return
    last_message_times[user_id] = time.time()
    if message.text:
        await bot.send_message(
            channel_id,
            f"{message.text.html}\n\nPosted by @{message.from_user.username}",
        )
    elif message.media:
        file_id = await bot.download_media(message)
        await bot.send_photo(
            channel_id,
            file_id,
            caption=f"{message.caption.html}\n\nPosted by @{message.from_user.username}",
        )
    else:
        print("This is document")
    user_message_count[user_id] = user_message_count.get(user_id, 0) + 1


async def start_bot():
    await bot.start()
    await bot.get_me()
    await bot.send_photo(
        chat_id,
        "https://telegra.ph/file/2707a66c92ba3c2e40cee.jpg",
        f"#START\n\nVersion:- α • 1.1\n\nYour Market Place Bot Has Been Started Successfully",
    )
    await idle()


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
