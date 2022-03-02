import os
import ytthumb
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
from youtubesearchpython import VideosSearch


Bot = Client(
    "YouTube-Search-Bot",
    bot_token = os.environ.get("BOT_TOKEN"),
    api_id = int(os.environ.get("API_ID")),
    api_hash = os.environ.get("API_HASH")
)


@Bot.on_message(filters.private & filters.all)
async def text(bot, update):
    
    text = "**Hello! 🙎\n\nI'm A simple Youtube Search Bot 💯💯.\n\nSearch 🔎 any Youtube Video  in telegram!\n\nYou must subscribe our channel in order to use me😇**"
    reply_markup = InlineKeyboardMarkup(
            [[
            InlineKeyboardButton(text="⭕️ CHANNEL ⭕️", url="https://t.me/Dads_links")], [InlineKeyboardButton(text="😇 SUPPORT", url="https://t.me/Dads_links_bot"),
                                                    InlineKeyboardButton(text="SHARE ♐️", url="https://t.me/share/url?url=https://t.me/Dads_links_youtube_Search_bot")]]),
            [InlineKeyboardButton(text="Search here 🔎", switch_inline_query_current_chat="")],
            [InlineKeyboardButton(text="Search in another chat 🔎", switch_inline_query="")]
            ]]
    )
    
    await update.reply_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def search(bot, update):
    
    results = VideosSearch(update.query, limit=50).result()
    answers = []
    
    for result in results:
        title = result["title"]
        views_short = result["viewCount"]["short"]
        duration = result["duration"]
        duration_text = result["accessibility"]["duration"]
        views = result["viewCount"]["text"]
        publishedtime = result["publishedTime"]
        channel_name = result["channel"]["name"]
        channel_link = result["channel"]["link"]
        description = f"{views_short} | {duration}"
        details = f"**Title:** {title}" + "\n" \
        f"**Channel:** [{channel_name}]({channel_link})" + "\n" \
        f"**Duration:** {duration_text}" + "\n" \
        f"**Views:** {views}" + "\n" \
        f"**Published Time:** {publishedtime}" + "\n" \
        "\n" + "**Made by @Doctorstra_1**"
        thumbnail = ytthumb.thumbnail(result["id"])
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Watch Video 📹", url=result["link"])]]
        )
        try:
            answers.append(
                InlineQueryResultPhoto(
                    title=title,
                    description=description,
                    caption=details,
                    photo_url=thumbnail,
                    reply_markup=reply_markup
                )
            )
        except:
            pass
    
    await update.answer(answers)


Bot.run()
