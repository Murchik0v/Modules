__version__ = (1, 0, 0)
# meta developer: @Murchik0v


import io

from requests import post

from .. import loader, utils  # pylint: disable=relative-beyond-top-level


@loader.tds
class envsMod(loader.Module):
    """Простой модуль для загрузки файлов на envs.sh"""

    strings = {"name": "Envs.sh Uploader"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def envscmd(self, message):
        await message.edit("<b><emoji document_id=5289930378885214069>✍️</emoji>Загрузка...</b>")
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b><emoji document_id=5258274739041883702>🔍</emoji>А где реплей на сообщение с файлом?</b>")
            return
        media = reply.media
        if not media:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "txt.txt"
        else:
            file = io.BytesIO(await self.client.download_file(media))
            file.name = (
                reply.file.name if reply.file.name else reply.file.id + reply.file.ext
            )
        try:
            envs = post("https://envs.sh", files={"file": file})
        except ConnectionError as e:
            await message.edit(ste(e))
            return
        url = envs.text
        output = f'<a href="{url}"><emoji document_id=5289862389552919154>🦋</emoji>Сыллка: </a><code>{url}</code>'
        await message.edit(output)