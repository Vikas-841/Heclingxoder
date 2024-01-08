from . import TGBot
import logging
import asyncio 
import time
import pickle 
import codecs 
import speedtest
from pyrogram import filters

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(name)

from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.errors import FloodWait
from datetime import datetime as dt

import SmartEncoder.Plugins.Labour
from SmartEncoder.Plugins.Queue import *
from SmartEncoder.Plugins.list import *
from SmartEncoder.Tools.eval import *
from SmartEncoder.Addons.download import d_l
from SmartEncoder.Addons.executor import bash_exec
from SmartEncoder.Plugins.cb import *
from SmartEncoder.Addons.list_files import l_s
from SmartEncoder.translation import Translation
from SmartEncoder.Tools.progress import *
from config import Config
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path

mode_for_custom = []
uptime = dt.now()
mode_for_custom.append("off")

# async def resume_task():
#   if myDB.llen("DBQueue") > 0:
#     queue_ = myDB.lindex("DBQueue", 0)
#     _queue = pickle.loads(codecs.decode(queue_.encode(), "base64"))
#     await add_task(TGBot, _queue)

async def start_bot():
    await TGBot.start()
    # await resume_task()
    await idle()

# if __name__ == "main":
#     loop.run_untill_complete(start_bot())
# rename_task.insert(0, "on")
if __name__ == "main":
    @TGBot.on_message(filters.incoming & (filters.video | filters.document))
    async def wah_1_man(bot, message: Message):
        if mode_for_custom[0] == "off":
            if message.chat.id not in Config.AUTH_USERS:
                return
            if rename_task[0] == "off":
                query = await message.reply_text("Aᴅᴅᴇᴅ ᴛʜɪs ғɪʟᴇ ɪɴ ǫᴜᴇᴜᴇ.\nCᴏᴍᴘʀᴇss ᴡɪʟʟ sᴛᴀʀᴛ sᴏᴏɴ.", quote=True)
                a = message
                data.append(a)
                if len(data) == 1:
                    await query.delete()
                    await add_task(bot, message)
            else:
                if message.from_user.id not in Config.AUTH_USERS:
                    return 
                query = await message.reply_text("Added this file to rename in queue.", quote=True)
                rename_queue.append(message)
                if len(rename_queue) == 1:
                    await query.delete()
                    await add_rename(bot, message)

    @TGBot.on_message(filters.incoming & filters.command("rename_mode", prefixes=["/", "."]))
    async def help_eval_message(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        OUT = "Rename Mode Has Been Enabled."
        await message.reply_text(OUT, quote=True)
        rename_task.insert(0, "on")

    @TGBot.on_message(filters.incoming & filters.command("eval", prefixes=["/", "."]))
    async def help_eval_message(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        await eval_handler(bot, message)

    @TGBot.on_message(filters.command("dl", prefixes=["/", "."]))
    async def start_cmd_handler(bot, update):
        if update.from_user.id not in Config.AUTH_USERS:
            return
        await d_l(bot, update)

    @TGBot.on_message(filters.command("ul", prefixes=["/", "."]))
    async def u_l(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        c_time = time.time()
        input_message = message.text.split(" ", maxsplit=1)[1]
        path = Path(input_message)
        if not os.path.exists(path):
            await message.reply_text(f"No such file or directory as {path} found", quote=True)
            return
        boa = await message.reply_text("UPLOADING", quote=True)
        await bot.send_document(
            chat_id=message.chat.id,
            document=path,
            force_document=True,
            reply_to_message_id=message.id,
            progress=progress_for_pyrogram,
            progress_args=(bot, "UPLOADING", boa, c_time)
        )
        await boa.delete()

    # bash
    @TGBot.on_message(filters.command("bash", prefixes=["/", "."]))
    async def start_cmd_handler(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        await bash_exec(bot, message)

    # ls
    @TGBot.on_message(filters.incoming & filters.command("ls", prefixes=["/", "."]))
    async def lost_files(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        await l_s(bot, message)

    # disable normal mode
    @TGBot.on_message(filters.command("manual_mode", prefixes=["/", "."]))
    async def hehe(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return 
        await message.reply_text("I will now wont respond to any file! Reply me with /dl and /ul", quote=True)
        mode_for_custom.insert(0, "on")

    # able normal mode
    @TGBot.on_message(filters.command("normal_mode", prefixes=["/", "."]))
    async def hehe(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return 
        await message.reply_text("I will now respond to any sent file", quote=True)
        mode_for_custom.insert(0, "off")
        rename_task.insert(0, "off")

    # start
    @TGBot.on_message(filters.command("start", prefixes=["/", "."]))
    async def start_cmd_handler(bot, message):
        await message.reply_text(
            text=Translation.START_TEXT,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📕𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url="https://t.me/Animes_Encoded")
                    ],
                ],
            )
        )

    # ping
    @TGBot.on_message(filters.incoming & filters.command(["ping"]))
    async def up(app, message):
        stt = dt.now()
        ed = dt.now()
        v = TimeFormatter(int((ed - uptime).seconds) * 1000)
        ms = (ed - stt).microseconds / 1000
        p = f"🌋Pɪɴɢ = {ms}ms"
        await message.reply_text(v + "\n" + p)

    # restart 
    @TGBot.on_message(filters.command("restart"))
    async def re(bot, message):
        if message.from_user.id in Config.AUTH_USERS:
            await message.reply_text("•Restarting")
            quit()

    # to change ffmpeg variables 
    @TGBot.on_message(filters.command("crf"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"I will be using : {cr} crf"
        crf.insert(0, f'{cr}')
        await message.reply_text(OUT, quote=True)

    @TGBot.on_message(filters.command("quality"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"I will be using : {cr} quality."
        qualityy.insert(0, f'{cr}')
        await message.reply_text(OUT, quote=True)

    @TGBot.on_message(filters.command("codec"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        if cr == "av1":
            OUT = f"<b>CODEC</b> ➺ <code>AV1</code>\n\nThis video codec has been successfully added to the <b>FFMPEG</b> code. Videos processed from now on will be using the said ffmpeg video codec.\n\n<b>NOTE</b> ➺ Please note that on applying <b>AV1</b> video codec, certain default ffmpeg integration changes."
            crf.insert(0, "48.5")
            qualityy.insert(0, "1280x720")
            preset.insert(0, "6")
            codec.insert(0, "av1")
        else:
            OUT = f"<b>CODEC</b> ➺ <code>{cr}</code>\n\nThis video codec has been successfully added to the <b>FFMPEG</b> code. Videos processed from now on will be using the said ffmpeg video codec."
            codec.insert(0, f'{cr}')
            crf.insert(0, "29")
            qualityy.insert(0, "846x480")
            bits.insert(0, "8")
            preset.insert(0, "medium")

        await message.reply_text(OUT, quote=True)

    @TGBot.on_message(filters.command("audio"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        _any = message.text.split(" ", maxsplit=1)[1]
        audio_.insert(0, f"{_any}")
        await message.reply_text(f"Fine! Your files are {_any} audio 👀", quote=True)

    @TGBot.on_message(filters.command("resolution"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"<b>I will use {cr} quality in renaming files<b>"
        quality_.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    @TGBot.on_message(filters.command("preset"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"I will use {cr} preset in encoding files."
        preset.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    # audio_mode ( for libopus and libfdk_aac support )
    @TGBot.on_message(filters.command("audio_codec"))
    async def re_codec_(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=2)[1]
        OUT = f"<b>I will use {cr} audio codec in encoding files.<b>"
        audio_codec.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    # watermark size
    @TGBot.on_message(filters.command("size"))
    async def re_codec_(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"<b>I will use {cr} watermark size in encoding files.<b>"
        watermark_size.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    # watermak text
    @TGBot.on_message(filters.command("text"))
    async def re_codec_(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"<b>I will use {cr} watermark text in encoding files.<b>"
        w_t.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    # bits
    @TGBot.on_message(filters.command("bits"))
    async def re_codec_(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"<b>I will use {cr} bits in encoding files.<b>"
        bits.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    # auth
    @TGBot.on_message(filters.command("auth"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"<b>ID</b> ➺ <code>{cr}</code>\n\nThis id has been successfully added to authorized chats.\n\n<b>NOTE</b> ➺ This id will be lost from the authorized chats as soon as the bot is restarted."
        Config.AUTH_USERS.append(int(cr))
        await message.reply_text(OUT, quote=True)

    # channel
    @TGBot.on_message(filters.command("channel"))
    async def re(bot, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"<b>I will add @{cr} channel username in renaming files<b>"
        CHANNEL_NAME.insert(0, f"{cr}")
        await message.reply_text(OUT, quote=True)

    # settings
    @TGBot.on_message(filters.incoming & filters.command(["settings"]))
    async def settings(app, message):
        if message.from_user.id in Config.AUTH_USERS:
            await message.reply_text(
                f"🏷 Video \n┏━━━━━━━━━━━━━━━━━\n┣ Codec  ➜ <code>{codec[0]}</code>\n┣ Crf  ➜ <code>{crf[0]}</code>\n┣ Resolution  ➜ <code>{qualityy[0]}</code>\n┣ Bits ➜ <code>{bits[0]}</code>\n┗━━━━━━━━━━━━━━━━━\n\n🏷  Audio \n┏━━━━━━━━━━━━━━━━━\n┣ Codec  ➜ <code>{audio_codec[0]}</code>\n┣  Bitrates ➜ <code>40k</code>\n┗━━━━━━━━━━━━━━━━━\n\n🏷 Watermark\n┏━━━━━━━━━━━━━━━━━\n┣ Text ➜ <code>{w_t[0]}</code>\n┣ Size  ➜ <code>{watermark_size[0]}</code>\n┗━━━━━━━━━━━━━━━━━\n\n🏷 Speed\n┏━━━━━━━━━━━━━━━━━\n┣ Preset ➜ <code>{preset[0]}</code>\n┗━━━━━━━━━━━━━━━━━",
                quote=True
            )

    # name
    @TGBot.on_message(filters.incoming & filters.command(["name"]))
    async def settings(app, message):
        if message.from_user.id not in Config.AUTH_USERS:
            return
        cr = message.text.split(" ", maxsplit=1)[1]
        OUT = f"Fine! I have set the name text to be {cr}"
        await message.reply_text(OUT, quote=True)
        name.insert(0, f"{cr}")

    # databases
    @TGBot.on_message(filters.incoming & filters.command("clear", prefixes=["/", "."]))
    async def lost_files(bot, message):
        if message.chat.id not in Config.AUTH_USERS:
            return
        data.clear()
        await message.reply_text("Successfully cleared queue.", quote=True)

    cb_bro = CallbackQueryHandler(
        cb_things
    )
    logger.info("Bot has started successfully 💀✊🏻")
    TGBot.add_handler(cb_bro)
    asyncio.get_event_loop().run_until_complete(start_bot())
    
