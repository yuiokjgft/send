#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)
from bot import (
    AUTH_CHANNEL,
    COMMM_AND_PRE_FIX,
    IS_BLACK_LIST_ED_MESSAGE_TEXT,
    START_COMMAND
)
from bot.hf.flifi import uszkhvis_chats_ahndler
from bot.sql.users_sql import (
    add_user_to_db
)
from bot.sql.blacklist_sql import (
    check_is_black_list
)

@Client.on_message(filters.regex(r"(/(?i)(t\.me|telegram\.(me|dog))\/joinchat/)", re.IGNORECASE))
async def hapus_linkjoin(_, message: Message):
    await message.reply_text(
            text="post gagal terkirim."
        )
    
@Client.on_message(filters.regex(r"((t\.me|telegram\.(dog|me))\/\w{5,}\?start=)", re.IGNORECASE))
async def hapus_linkrefferal(_, message: Message):
    await message.reply_text(
            text="post gagal terkirim. link refferal bot tidak di perbolehkan"
        )
    
@Client.on_message(
    ~filters.command(START_COMMAND, COMMM_AND_PRE_FIX) &
    ~uszkhvis_chats_ahndler([AUTH_CHANNEL]) &
    filters.incoming
)
async def on_pm_s(_, message: Message):
    check_ban = check_is_black_list(message)
    if check_ban:
        await message.reply_text(
            text=IS_BLACK_LIST_ED_MESSAGE_TEXT.format(
                reason=check_ban.reason
            )
        )
        return
    
    if message.text is not None and len(message.text.split()) == 1:
        await message.reply(
        text="post gagal terkirim"
        )
        return
    
    if message.edit_date:
        await message.reply_text(
            text="mengedit post tidak akan mengubah pesan di channel"
        )
        return

    if message.sticker or message.animation:
        await message.reply_text(
            text="post gagal terkirim sticker ataupun gif tidak di perbolehkan"
        )
        return
    
    if message.forward_from_chat or message.forward_date:
        await message.reply_text(
            text="post gagal terkirim"
        )
        return
    
    if (message.photo or message.video) and message.caption is None:
        await message.reply_text(
            text="post gagal terkirim."
        )
        return
    
    if message.text and message.entities and message.entities[0].type == "bot_command" and len(message.text) == message.entities[0].length: 
        await message.reply_text(
            text="bot command detected, post gagal terkirim"
        )
        return
    
    #if ((message.photo or message.video or message.voice or message.video_note or message.audio or message.document) and message.caption) is not None:
       # text = ((message.photo or message.video or message.voice or message.video_note or message.audio or message.document) and message.caption)
    #if message.text is not None:
        #text = message.text
    #username = re.findall(r"@[\w]{5,32}", text)
    #for i in username:
        #uname = i.replace("@", "")
        #try:
            #chat = await _.get_chat(uname)
        #except Exception as e:
            #return await message.reply("channel username kosong")
        #if chat.type == "channel":
            #return await message.reply("channel username detected")
    
    if message.text is not None :
        username = re.findall(r"@[\w]{5,32}", message.text)
        for i in username:
            uname = i.replace("@", "")
            try:
                chat = await _.get_chat(uname)
            except Exception as e:
                return await message.reply("channel username kosong")
            if chat.type == "channel":
                return await message.reply("channel username detected")
     
    if message.caption is not None :
        username = re.findall(r"@[\w]{5,32}", message.caption)
        for i in username:
            uname = i.replace("@", "")
            try:
                chat = await _.get_chat(uname)
            except Exception as e:
                return await message.reply("channel username kosong")
            if chat.type == "channel":
                return await message.reply("channel username detected")
    
    fwded_mesg = await message.forward(
        AUTH_CHANNEL, as_copy=True
    )

    add_user_to_db(
        fwded_mesg.message_id,
        message.from_user.id,
        message.message_id
    )
