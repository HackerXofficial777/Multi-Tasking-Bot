import pyrogram, asyncio, random, time, os
from pyrogram import Client, filters, enums
from pyrogram.types import *
from helper.database import adds_user, db
from info import * #PICS, LOG_TEXT, LOG_CHANNEL 
from helper.text import txt
from pyrogram.errors import UserNotParticipant, ChatAdminRequired

@Client.on_message(filters.private & filters.command("start"))
async def start_message(bot, message):
    user_id = message.from_user.id
    not_joined = []

    # Check multiple channel subscription
    for channel in FORCE_SUB_CHANNELS:
        try:
            await bot.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except ChatAdminRequired:
            return await message.reply_text(f"❌ I don't have permission to check users in `{channel}`. Make me admin.")

    if not_joined:
        buttons = []
        for ch in not_joined:
            buttons.append([InlineKeyboardButton(f"✅ Join {ch}", url=f"https://t.me/{ch}")])
        buttons.append([InlineKeyboardButton("♻️ Check Again", callback_data="refreshMultiSub")])

        return await message.reply_text(
            "**To use this bot, you must join all required channels first:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Save user if new
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
        if LOG_CHANNEL:
            await bot.send_message(LOG_CHANNEL,
                text=LOG_TEXT.format(
                    id=user_id,
                    dc_id=message.from_user.dc_id,
                    first_name=message.from_user.first_name,
                    username=message.from_user.username,
                    bot=bot.mention
                )
            )

    # Send main welcome message
    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton("⚙️ ꜱᴜᴩᴩᴏʀᴛ", url="https://t.me/silicon_Botz")
    ], [
        InlineKeyboardButton("⚡ ʜᴇʟᴩ", callback_data="help"),
        InlineKeyboardButton("📃 ᴀʙᴏᴜᴛ", callback_data="about")
    ], [
        InlineKeyboardButton("📢 ᴜᴩᴅᴀᴛᴇꜱ", url="https://t.me/Silicon_Bot_Update")
    ]])

    await message.reply_photo(
        photo=random.choice(PICS),
        caption=txt.STAT.format(message.from_user.mention),
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex("refreshMultiSub"))
async def recheck_multi_sub(bot, query):
    user_id = query.from_user.id
    not_joined = []

    for channel in FORCE_SUB_CHANNELS:
        try:
            await bot.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)

    if not_joined:
        buttons = []
        for ch in not_joined:
            buttons.append([InlineKeyboardButton(f"✅ Join {ch}", url=f"https://t.me/{ch}")])
        buttons.append([InlineKeyboardButton("♻️ Check Again", callback_data="refreshMultiSub")])

        await query.message.edit_text(
            "**You still need to join all required channels:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await query.answer("❌ You haven't joined all required channels.", show_alert=True)
    else:
        await query.message.delete()
        await start_message(bot, query.message)

                                              
@Client.on_message(filters.command(["id", "info"]))
async def media_info(bot, m): 
    message = m
    ff = m.from_user
    md = m.reply_to_message
    if md:
       try:
          if md.photo:
              await m.reply_text(text=f"**ʏᴏᴜʀ ᴘʜᴏᴛᴏ ɪᴅ ɪs **\n\n`{md.photo.file_id}`") 
          if md.sticker:
              await m.reply_text(text=f"**ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ɪᴅ ɪs**\n\n`{md.sticker.file_id}`")
          if md.video:
              await m.reply_text(text=f"**ʏᴏᴜʀ ᴠɪᴅᴇᴏ ɪᴅ ɪs**\n\n`{md.video.file_id}`")
          if md.document:
              await m.reply_text(text=f"**ʏᴏᴜʀ ᴅᴏᴄᴜᴍᴇɴᴛ ɪᴅ ɪs**\n\n`{md.document.file_id}`")
          if md.audio:
              await m.reply_text(text=f"**ʏᴏᴜʀ ᴀᴜᴅɪᴏɴ ɪᴅ ɪs**\n\n`{md.audio.file_id}`")
          if md.text:
              await m.reply_text("**ʜᴇʏ ʙʀᴏᴛʜᴇʀ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴡɪᴛʜ ( ᴘʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, sᴛɪᴄᴋᴇʀ, ᴅᴏᴄᴜᴍᴇɴᴛs, ᴇᴛᴄ...) ᴏɴʟʏ ᴍᴇᴅɪᴀ**")  
          else:
              await m.reply_text("[404] ᴇʀʀᴏʀ..🤖")                                                                                      
       except Exception as e:
          print(e)
          await m.reply_text(f"[404] Error {e}")
                                        
    if not md:
        buttons = [[
            InlineKeyboardButton("✨️ sᴜᴘᴘᴏʀᴛ", url="https://t.me/silicon_botz"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/silicon_Bot_Update")
        ]]       
        silicon = await m.reply("please wait....")
        if ff.photo:
           user_dp = await bot.download_media(message=ff.photo.big_file_id)
           await m.reply_photo(
               photo=user_dp,
               caption=txt.INFO_TXT.format(id=ff.id, dc=ff.dc_id, n=ff.first_name, u=ff.username),
               reply_markup=InlineKeyboardMarkup(buttons),
               quote=True,
               parse_mode=enums.ParseMode.HTML,
               disable_notification=True
           )          
           os.remove(user_dp)
           await silicon.delete()
        else:  
           await m.reply_text(
               text=txt.INFO_TXT.format(id=ff.id, dc=ff.dc_id, n=ff.first_name, u=ff.username),
               reply_markup=InlineKeyboardMarkup(buttons),
               quote=True,
               parse_mode=enums.ParseMode.HTML,
               disable_notification=True
           )

 