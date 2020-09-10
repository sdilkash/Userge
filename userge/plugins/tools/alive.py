# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram.errors import ChatSendMediaForbidden
from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest, ChannelInvalid, MediaEmpty

from userge.core.ext import RawClient
from userge import userge, Message, Config, versions, get_version

LOGO_ID, LOGO_REF = None, None


@userge.on_cmd("alive", about={
    'header': "This command is just for fun"}, allow_channels=False)
async def alive(message: Message):
    await message.delete()
    output = f"""
    print("⫷𝓘'𝓶  𝓪𝓵𝓲𝓿𝓮  𝓱𝓮𝓻𝓮  𝓓𝓘𝓛𝓚𝓐𝓢𝓗⫸");
**⌚ Up Time** : `{userge.uptime}`
**💥 Version** : `{get_version()}`

**🎇 Sudo**: `{_parse_arg(Config.SUDO_ENABLED)}`
**🎇 Anti-Spam**: `{_parse_arg(Config.ANTISPAM_SENTRY)}`
**🎇 Dual-Mode**: `{_parse_arg(RawClient.DUAL_MODE)}`"""
    if Config.HEROKU_APP:
        output += f"\n• **dyno-saver**: `{_parse_arg(Config.RUN_DYNO_SAVER)}`"
    output += f"""
**🎇 Unofficial**: `{_parse_arg(Config.LOAD_UNOFFICIAL_PLUGINS)}`

   **🌹 __Python__**: `{versions.__python_version__}`
   **🌹 __Pyrogram__**: `{versions.__pyro_version__}`

**{versions.__license__}** | **{versions.__copyright__}** | **[Repo]({Config.UPSTREAM_REPO})**
"""
    print("User Name:〘 𝔻ᶤ𝕃Ҝⓐ𝕊ℍ 】");
    print("🌹🌹🌹🌹🌹💐🌹🌹🌹🌹🌹");
    try:
        await _send_alive(message, output)
    except (FileIdInvalid, FileReferenceEmpty, BadRequest):
        await _refresh_id()
        await _send_alive(message, output)


def _parse_arg(arg: bool) -> str:
    return "enabled" if arg else "disabled"


async def _send_alive(message: Message, text: str) -> None:
    if not (LOGO_ID and LOGO_REF):
        await _refresh_id()
    try:
        await message.client.send_animation(chat_id=message.chat.id,
                                            animation=LOGO_ID,
                                            file_ref=LOGO_REF,
                                            caption=text)
    except (MediaEmpty, ChatSendMediaForbidden):
        await message.client.send_message(chat_id=message.chat.id,
                                          text=text,
                                          disable_web_page_preview=True)


async def _refresh_id():
    global LOGO_ID, LOGO_REF  # pylint: disable=global-statement
    try:
        gif = (await userge.get_messages('-1001260319807', 394429)).animation
    except ChannelInvalid:
        LOGO_ID = None
        LOGO_REF = None
    else:
        LOGO_ID = gif.file_id
        LOGO_REF = gif.file_ref
