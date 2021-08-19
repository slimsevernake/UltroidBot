# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}saavn <search query>`
    Download songs from Saavn

"""
import os
import time
from urllib.request import urlretrieve

import requests as r
from telethon.tl.types import DocumentAttributeAudio

from . import *


@ultroid_cmd(
    pattern="saavn ?(.*)",
)
async def siesace(e):
    song = e.pattern_match.group(1)
    if not song:
        return await eod(e, "`Give me Something to Search")
    hmm = time.time()
    lol = await eor(e, f"`Searching {song} on Saavn...`")
    sung = song.replace(" ", "%20")
    url = f"https://jostapi.herokuapp.com/saavn?query={sung}"
    try:
        k = (r.get(url)).json()[0]
    except IndexError:
        return await eod(lol, "`Song Not Found.. `")
    except Exception as ex:
        return await eod(lol, f"`{str(ex)}`")
    try:
        title = k["song"]
        urrl = k["media_url"]
        img = k["image"]
        duration = k["duration"]
        singers = k["primary_artists"]
    except Exception as ex:
        return await eod(lol, f"`{ex}`")
    song = await fast_download(urrl, file_name=title + ".mp3")
    thumb = await fast_download(img, file_name=title + ".jpg")
    okk = await uploader(song, song, hmm, lol, "Uploading " + title + "...")
    await e.reply(
        file=okk,
        message="`" + title + "`" + "\n`From Saavn`",
        attributes=[
            DocumentAttributeAudio(
                duration=int(duration),
                title=title,
                performer=singers,
            )
        ],
        supports_streaming=True,
        thumb=thumb,
    )
    await lol.delete()
    [os.remove(x) for x in [song, thumb]]
