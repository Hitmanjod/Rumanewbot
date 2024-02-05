import time
import asyncio
import logging
import time
from pyrogram import filters

from ..Config import *
from ..core.clients import app

last_message_times = {}
user_message_count = {}
message_queue = {}
allowed_user_id = SUDO_USERS.split(" ")


@app.on_message(filters.chat(CHAT_ID) & ~filters.bot & ~filters.service)
async def forward_handler(bot, message):
    user_id = message.from_user.id
    reply_id = (
        message.reply_to_message.from_user.id if message.reply_to_message else None
    )
    max_posts_per_day = MAX_POSTS_PER_DAY
    if message.text == "/sub":
        if reply_id:
            if user_message_count.get(reply_id, 0) >= int(max_posts_per_day):
                remaining_posts = 0
            else:
                remaining_posts = int(max_posts_per_day) - user_message_count.get(
                    reply_id, 0
                )
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(reply_id, 0)}"
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
    textss = (
        message.text.startswith(".") or message.text.startswith("/")
        if message.text
        else None
    )
    if textss:
        pass
    if message.chat.id in last_message_times:
        if str(user_id) in str(allowed_user_id):
            last_message_times[user_id] = time.time()
        else:
            if user_message_count.get(user_id, 0) >= int(max_posts_per_day):
                return await message.reply_text(
                    "Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit."
                )
        time_since_last_message = time.time() - last_message_times[message.chat.id]
        if time_since_last_message < int(max_time):
            remaining_time = int(max_time) - time_since_last_message
            cooldown_message = f"Please wait {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds before posting another message to the channel.\n\n**Your post is added to queue & will be posted after {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds automatically.**"
            await message.reply_text(cooldown_message)
            message_queue.update({message.id: [user_id, message.chat.id]})
            await asyncio.sleep(remaining_time)
            for key, value in message_queue.items():
                usrid = value[0]
                value[1]
                qu_max_posts_per_day = max_posts
                if user_message_count.get(usrid, 0) >= int(qu_max_posts_per_day):
                    await message.reply_text(
                        "Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit."
                    )
                    continue
                if message.text:
                    try:
                        await bot.send_message(
                            CHANNEL_ID,
                            f"{message.text.html}\n\nPosted by @{message.from_user.username}",
                        )
                    except Exception as e:
                        print(f"Error in {id} : {e}")
                elif message.photo:
                    file_id = message.photo.file_id
                    caption = message.caption.html if message.caption else ""
                    try:
                        await bot.send_photo(
                            CHANNEL_ID,
                            file_id,
                            caption=f"{caption}\n\nPosted by @{message.from_user.username}",
                        )
                    except Exception as e:
                        print(f"Error in {id} : {e}")
                elif message.animation:
                    file_id = message.animation.file_id
                    caption = message.caption.html if message.caption else ""
                    try:
                        await bot.send_animation(
                            CHANNEL_ID,
                            file_id,
                            caption=f"{caption}\n\nPosted by @{message.from_user.username}",
                        )
                    except Exception as e:
                        print(f"Error in {id} : {e}")
                elif message.document:
                    file_id = message.document.file_id
                    caption = message.caption.html if message.caption else ""
                    try:
                        await bot.send_document(
                            CHANNEL_ID,
                            file_id,
                            caption=f"{caption}\n\nPosted by @{message.from_user.username}",
                        )
                    except Exception as e:
                        print(f"Error in {id} : {e}")
                else:
                    print("This is something else")
                user_message_count[usrid] = user_message_count.get(usrid, 0) + 1
                await asyncio.sleep(600)
            message_queue.clear()
            return
    last_message_times[message.chat.id] = time.time()
    if message.text:
        try:
            await bot.send_message(
                CHANNEL_ID,
                f"{message.text.html}\n\nPosted by @{message.from_user.username}",
            )
        except Exception as e:
            print(f"Error in {id} : {e}")
    elif message.photo:
        file_id = message.photo.file_id
        caption = message.caption.html if message.caption else ""
        try:
            await bot.send_photo(
                CHANNEL_ID,
                file_id,
                caption=f"{caption}\n\nPosted by @{message.from_user.username}",
            )
        except Exception as e:
            print(f"Error in {id} : {e}")
    elif message.animation:
        file_id = message.animation.file_id
        caption = message.caption.html if message.caption else ""
        try:
            await bot.send_animation(
                CHANNEL_ID,
                file_id,
                caption=f"{caption}\n\nPosted by @{message.from_user.username}",
            )
        except Exception as e:
            print(f"Error in {id} : {e}")
    elif message.document:
        file_id = message.document.file_id
        caption = message.caption.html if message.caption else ""
        try:
            await bot.send_document(
                CHANNEL_ID,
                file_id,
                caption=f"{caption}\n\nPosted by @{message.from_user.username}",
            )
        except Exception as e:
            print(f"Error in {id} : {e}")
    else:
        print("This is document")
    user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
