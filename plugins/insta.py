import requests
from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command(["instadl", "insdl", "insta", "instadownload"]))
async def igdownload(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please provide an Instagram URL 🤦‍♂️**")
    
    url = message.text.split(None, 1)[1]
    msg = await message.reply_text("**Downloading... 📤**")

    try:
        response = requests.get(f"https://horridapi.onrender.com/instadl?url={url}", timeout=10)
        
        if response.status_code != 200 or not response.content:
            await msg.edit("**API is not responding or returned an error. Try again later.**")
            return

        data = response.json()

        if data.get("STATUS") != "OK" or "result" not in data:
            await msg.edit("**Invalid or unsupported Instagram URL.**")
            return

        result = data["result"]
        media = []

        for s in result:
            if s.get("media") == "image":
                media.append(InputMediaPhoto(media=s.get("url")))
            elif s.get("media") == "video":
                media.append(InputMediaVideo(media=s.get("url")))

        if not media:
            await msg.edit("**No valid media found to send.**")
            return

        await message.reply_media_group(media=media)
        await msg.delete()

    except requests.exceptions.RequestException as e:
        await msg.edit(f"**Network error occurred:** `{str(e)}`")
    except Exception as e:
        await msg.edit(f"**Unexpected error:** `{str(e)}`")
        
