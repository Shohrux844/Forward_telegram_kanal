import asyncio
from telethon import TelegramClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramContentDownloader:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('new_session', api_id, api_hash)

    async def forward_new_messages_forever(self, source_channel, target_channel):
        """
        Yangi xabar kelishini doimiy kuzatadi.
        Matndagi @MILITSIYA_UZB ni @top_tovar_lid ga almashtirib yuboradi.
        Media fayllar ham qo‘shib yuboriladi.
        """
        try:
            await self.client.start(phone=self.phone_number)
            logger.info("Telegram clientga ulanildi")

            source_entity = await self.client.get_entity(source_channel)
            target_entity = await self.client.get_entity(target_channel)

            logger.info(f"Manba kanal: {source_entity.title}")
            logger.info(f"Maqsad kanal: {target_entity.title}")

            last_message_id = 0

            while True:
                messages = await self.client.get_messages(source_entity, limit=10)
                messages = list(reversed(messages))

                for message in messages:
                    if message.id <= last_message_id:
                        continue

                    if message.message or message.media:
                        try:
                            # Matndagi kanal nomini almashtirish
                            text = message.text or ""

                            text = text.replace("@MILITSIYA_UZB", "@Manba_Uz")
                            text = text.replace("@Militsiya_Uzb👈🏽", "@manba_uz_lid👈🏽")

                            # Media bor bo‘lsa birga yuborish
                            if message.media:
                                await self.client.send_file(
                                    entity=target_entity,
                                    file=message.media,
                                    caption=text
                                )
                            else:
                                await self.client.send_message(
                                    entity=target_entity,
                                    message=text
                                )

                            logger.info(f"#{message.id} xabar yuborildi")
                            last_message_id = message.id
                            await asyncio.sleep(2)

                        except Exception as e:
                            logger.error(f"Xatolik: {e}")
                            continue

                await asyncio.sleep(10)

        except Exception as e:
            logger.error(f"Xatolik yuz berdi: {str(e)}")
        finally:
            await self.client.disconnect()


async def main():
    API_ID = 28238713
    API_HASH = "2fe45b820543aa4875ada70d0ff31491"
    PHONE_NUMBER = "+998990009031"

    downloader = TelegramContentDownloader(API_ID, API_HASH, PHONE_NUMBER)

    await downloader.forward_new_messages_forever(
        source_channel="@MILITSIYA_UZB",
        target_channel="@manba_uz_lid"
    )


if __name__ == "__main__":
    asyncio.run(main())