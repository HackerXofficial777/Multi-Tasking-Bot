from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import requests, traceback
from info import SPIDEY_CHANNEL as DUMP_GROUP

@Client.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    m = await message.reply_sticker("CAACAgUAAxkBAAITAmWEcdiJs9U2WtZXtWJlqVaI8diEAAIBAAPBJDExTOWVairA1m8eBA")

    try:
        api = "https://alphaapis.org/Instagram/dl/v1"
        response = requests.get(api, params={"url": link})

        if response.ok:
            data = response.json()
            if data.get("success") and data.get("result"):
                media = data["result"][0]
                video_url = media.get("downloadLink")
                caption = data.get("caption") or "No caption available."
                stats = data.get("statistics") or {}

                views = str(stats.get("views", 0))
                likes = str(stats.get("likes", 0))
                comments = str(stats.get("comments", 0))

                like_cb = f"alert_like_{likes}"
                comment_cb = f"alert_comment_{comments}"
                view_cb = f"alert_view_{views}"

                buttons = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(f"❤️ {likes}", callback_data=like_cb),
                        InlineKeyboardButton(f"💬 {comments}", callback_data=comment_cb),
                        InlineKeyboardButton(f"👁 {views}", callback_data=view_cb)
                    ],
                    [
                        InlineKeyboardButton("⬇️ Download Again", url=video_url)
                    ]]
                )

                if "story" in media.get("type", "").lower():
                    sent = await message.reply_video(
                        video_url,
                        caption=f"<b>Instagram Story</b>\n\n<b><blockquote>🌿 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href='https://telegram.me/spidey_multi_tasking_robot'>@sᴘɪᴅᴇʏ_ᴍᴜʟᴛɪ_ᴛᴀsᴋɪɴɢ_ʀᴏʙᴏᴛ</a></blockquote></b>",
                        reply_markup=buttons
                    )
                else:
                    sent = await message.reply_video(
                        video_url,
                        caption=f"<b>{caption}</b>\n\n<b><blockquote>🌿 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href='https://telegram.me/spidey_multi_tasking_robot'>@sᴘɪᴅᴇʏ_ᴍᴜʟᴛɪ_ᴛᴀsᴋɪɴɢ_ʀᴏʙᴏᴛ</a></blockquote></b>",
                        reply_markup=buttons
                    )

                if DUMP_GROUP:
                    await sent.copy(DUMP_GROUP)
                return

        await message.reply("Oops! ⚠️ Failed to fetch — Please try again later! ✨")

    except Exception as e:
        await message.reply(f"<b>400: 🚫 Error:</b> {str(e)}")
        if DUMP_GROUP:
            await Mbot.send_message(DUMP_GROUP, f"Instagram Error: {e}\n{traceback.format_exc()}")
    finally:
        if 'm' in locals():
            await m.delete()


@Client.on_callback_query(filters.regex("^alert_"))
async def insta_callback_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    if "like" in data:
        await callback_query.answer(f"❤️ Likes: {data.split('_')[-1]}", show_alert=True)
    elif "comment" in data:
        await callback_query.answer(f"💬 Comments: {data.split('_')[-1]}", show_alert=True)
    elif "view" in data:
        await callback_query.answer(f"👁 Views: {data.split('_')[-1]}", show_alert=True)
