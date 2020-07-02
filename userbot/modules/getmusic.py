# Copyright (C) 2020 Aidil Aryanto.
# All rights reserved.

import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot, CMD_HELP, lastfm, LASTFM_USERNAME
from userbot.events import register
from pylast import User

@register(outgoing=True, pattern=r"^\.songn (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit(
                "`Error: No current scrobble found.`"
            )
        artist = playing.get_artist()
        song = playing.get_title()
        track = str(artist) + " - " + str(song)
    else:
        track = event.pattern_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {track}"
    await event.edit("`Searching...`")
    async with bot.conversation(chat) as conv:
          await asyncio.sleep(2)
          await event.edit("`Downloading...Please wait`")
          try:
              msg = await conv.send_message(link)
              response = await conv.get_response()
              respond = await conv.get_response()
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError:
              await event.reply("```Please unblock @WooMaiBot and try again```")
              return
          await event.edit("`Sending Your Music...`")
          await asyncio.sleep(3)
          await bot.send_file(event.chat_id, respond)
    await event.client.delete_messages(conv.chat_id,
                                       [msg.id, response.id, respond.id])
    await event.delete()

@register(outgoing=True, pattern=r"^\.songl(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("`Enter a valid link to download from`")
    else:
        await event.edit("`Downloading...`")
    chat = "@MusicHuntersBot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            response = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            song = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("`Unblock `@MusicHuntersBot` and retry`")
            return
        await bot.send_file(event.chat_id, song, caption=details.text)
        await event.client.delete_messages(conv.chat_id,
                                           [msg_start.id, response.id, msg.id, details.id, song.id])
        await event.delete()


@register(outgoing=True, pattern=r"^\.songf (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit(
                "`Error: No scrobbling data found.`"
            )
        artist = playing.get_artist()
        song = playing.get_title()
        track = str(artist) + " - " + str(song)
    else:
        track = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit("`Downloading...`")
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True, from_users=752979930))
            msg = await bot.send_message(chat, track)
            respond = await response
            res = conv.wait_event(events.NewMessage(
                incoming=True, from_users=752979930))
            r = await res
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply("`Unblock `@SpotifyMusicDownloaderBot` and retry`")
            return
        await bot.forward_messages(event.chat_id, respond.message)
    await event.client.delete_messages(conv.chat_id,
                                       [msg.id, r.id, respond.id])
    await event.delete()

CMD_HELP.update({
    "getmusic":
    ">`.songn <Artist - Song Title>`"
    "\nUsage: Download music by name"
    "\n\n>`.songl <Spotify/Deezer Link>`"
    "\nUsage: Download music by link"
    "\n\n>`.songf <Artist - Song Title>`"
    "\nUsage: Download music by name (fallback)"
    "\n\n>`.songn now`"
    "\nUsage: Download current LastFM scrobble"
    "\n\n>`.songf now`"
    "\nUsage: Download current LastFM scrobble (fallback)"
})
