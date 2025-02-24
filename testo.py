from telethon import TelegramClient, events
import asyncio
import logging
import requests
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
import sys
import time

API_ID = 23478555
API_HASH = '64b6da1fbb19a4af790a3c5f6b83e49a'
PHONE_NUMBER = '905355825662'

logging.basicConfig(level=logging.INFO)

# رقم صاحب الحساب
OWNER_PHONE = '905355825662'  # تأكد من أن هذا الرقم هو الرقم المسموح به فقط
DEVELOPER_ID = 6988477775

# تأثير تحميل
async def show_loading_message(event):
    loading_message = await event.reply('🔄 جاري تحميل الفيديو...')
    for i in range(10):
        await asyncio.sleep(1)
        await loading_message.edit(f'🔄 جاري تحميل الفيديو{"." * (i % 3 + 1)}')
    return loading_message

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)

    @client.on(events.NewMessage(pattern='تست'))
    async def stick_handler(event):
        # تحقق إذا كان الرقم هو المطور فقط
        if str(event.sender_id) != str(DEVELOPER_ID):
            await event.reply('❌ هذا الأمر مخصص للمطور فقط.')
            return
        await event.reply('✅ البوت يعمل بشكل صحيح!')

  

    @client.on(events.NewMessage(pattern='جلب (.*) (.*)'))
    async def handler(event):
        # تحقق إذا كان الرقم هو المطور فقط
        if str(event.sender_id) != str(DEVELOPER_ID):
            await event.reply('❌ هذا الأمر مخصص للمطور فقط.')
            return

        url = event.pattern_match.group(1)
        description = event.pattern_match.group(2)
        try:
            if "/c/" in url:
                parts = url.split("/")
                chat_id = int("-100" + parts[-2])  
                message_id = int(parts[-1])  
                entity = await client.get_entity(PeerChannel(chat_id))
            else:
                entity = await client.get_entity(url)
                message_id = None 
        except ValueError as e:
            await client.send_message('me', f'صفائتي حبيبتي تاكدي من انك كاتبة الاسم مع فراغ وملصوق ببعضه طيب؟')
            return
        except Exception as e:
            await client.send_message('me', f'صفاااء ما عبقدر انزله بسبب اني ما عبقدر اوصل للرسالة!!')
            return
        try:
            messages = await client(GetHistoryRequest(
                peer=entity,
                limit=1,
                offset_id=message_id,  
                offset_date=None,
                add_offset=0,
                max_id=message_id,
                min_id=0,
                hash=0
            ))
            loading_message = await show_loading_message(event)
            for message in messages.messages:
                if message.media and message.media.video:
                    await client.send_file('me', message.media, caption=description)
                    await loading_message.edit(f'✅ تم إرسال الفيديو إلى الرسائل المحفوظة: {description}')
                else:
                    await loading_message.edit(f'⚠️ لا يوجد فيديو في الرسالة: {url}')
                    await client.send_message('me', f'⚠️ لا يوجد فيديو في الرسالة: {url}')
        except Exception as e:
            await client.send_message('me', f'❌ حدث خطأ أثناء جلب الفيديو: {e}')

    try:
        print("✅ البوت قيد التشغيل... اضغط Ctrl+C للإيقاف.")
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        print("⏹️ تم إيقاف البوت يدويًا.")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
    finally:
        await client.disconnect()
        print("🔴 تم إغلاق الاتصال بنجاح.")

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
