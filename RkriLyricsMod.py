# 
# ████──█──█──████──███───────█───██─████──████───█─█──█────███──███
# █──█──█─█───█──█───█────────██─███─█──█──█──██──█─█──█────█────█
# ████──██────████───█────────█─█─██─█──█──█──██──█─█──█────███──███
# █─█───█─█───█─█────█────────█───██─█──█──█──██──█─█──█────█──────█
# █─█───█──█──█─█───███───────█───██─████──████───███──███──███──███
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0
# meta developer: rkri_modules
# meta pic: https://img.icons8.com/emoji/256/musical-notes-emoji.png

import logging
from telethon.tl.types import Message, DocumentAttributeAudio
from .. import loader, utils, translations
import requests


logger = logging.getLogger(__name__)


@loader.tds
class GLyricsMod(loader.Module):
    """Get lyrics from Genius"""
    strings = {
        "name": "GLyrics",
        "lyrics": "📝 <b>Lyrics</b> for <b>{}</b>:\n\n{}",
        "no_lyrics": "😔 <b>No lyrics</b> for <b>{}</b> or something else happened.",
        "args?": "😶 <b>What song do you want lyrics for?</b>",
        "wait": "🧐 <b>Searching for lyrics...</b>",
        "full_text": "👀 View full lyrics",
    }

    strings_ru = {
        "name": "GLyrics",
        "lyrics": "📝 <b>Текст песни</b> <b>{}</b>:\n\n{}",
        "no_lyrics": "😔 <b>Текста песни</b> для <b>{}</b> нет или что-то пошло не так.",
        "args?": "😶 <b>Какую песню вы хотите найти?</b>",
        "wait": "🧐 <b>Ищу текст песни...</b>",
        "full_text": "👀 Посмотреть полный текст",
        "_cls_doc": "Ищет тексты песен в Genius",
        "_cmd_doc_lyrics": "Найти текст песни"
    }

    strings_de = {
        "name": "GLyrics",
        "lyrics": "📝 <b>Lyrics</b> für <b>{}</b>:\n\n{}",
        "no_lyrics": "😔 <b>Kein Lyrics</b> für <b>{}</b> oder etwas anderes ist passiert.",
        "args?": "😶 <b>Welchen Song willst du Lyrics für haben?</b>",
        "wait": "🧐 <b>Suche nach Lyrics...</b>",
        "full_text": "👀 Vollständigen Text anzeigen",
        "_cls_doc": "Sucht nach Lyrics auf Genius",
        "_cmd_doc_lyrics": "Suche nach Lyrics"
    }

    async def lyricscmd(self, m: Message):
        """Search for lyrics"""
        r = await m.get_reply_message()
        if not utils.get_args_raw(m) and not r:
            return await utils.answer(m, self.strings("args?"))
        if r and not utils.get_args_raw(m):
            if not r.media:
                return await utils.answer(m, self.strings("args?"))
            attr = r.media.document.attributes[0]
            if not isinstance(attr, DocumentAttributeAudio):
                return await utils.answer(m, self.strings("args?"))
            song = f'{attr.performer} - {attr.title}'
        else:
            song = utils.get_args_raw(m)

        await utils.answer(m, self.strings("wait"))

        try:
            data = {'name': song}
            r = requests.post(f"https://tzj9cc.deta.dev/mirror/genius/lyrics", json=data)
            r = r.json()
            lyrics = r["res"]["lyrics"]
            title = r["res"]["name"]
            full_link = r["res"]["url"]

            await self.inline.form(
                self.strings("lyrics").format(title, lyrics),
                reply_markup=[[{"text": self.strings["full_text"], "url": full_link}]],
                message=m,
                force_me=False

            )
        except Exception as e:
            logger.error(e)
            await utils.answer(m, self.strings("no_lyrics").format(song))
