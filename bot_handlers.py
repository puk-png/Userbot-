import asyncio
import random
import re
import speech_recognition as sr
import requests
import io
import os
import tempfile
import subprocess
from telethon import events, functions, types
from config import CHANNEL_ID, KEYWORDS_FOR_HEART

class BotStatus:
    def __init__(self):
        self.is_running = False
        self.last_error: str | None = None
        self.commands_processed = 0
        self.reactions_sent = 0
        self.messages_processed = 0

status = BotStatus()

def register_handlers(client):
    """Register all bot event handlers"""
    
    @client.on(events.NewMessage(pattern=r'/gayporn|/random'))
    async def send_random_from_channel(event):
        """Відправляє випадкове повідомлення з каналу"""
        try:
            status.commands_processed += 1
            print(f"Processing /random command from user {event.sender_id}")
            
            # Отримуємо останні 100000 повідомлень з каналу
            messages = []
            async for message in client.iter_messages(CHANNEL_ID, limit=100000):
                if message.text or message.media:
                    messages.append(message)
            
            if messages:
                random_message = random.choice(messages)
                print(f"Sending random message: {random_message.id}")
                
                # Пересилаємо повідомлення як reply
                if random_message.media:
                    await event.reply(file=random_message.media, message=random_message.text or "")
                else:
                    await event.reply(random_message.text)
            else:
                await event.reply("❌ Не знайдено повідомлень у каналі")
                
        except Exception as e:
            error_msg = f"Помилка: {str(e)}"
            status.last_error = error_msg
            print(f"Error in random command: {e}")
            await event.reply(error_msg)

    @client.on(events.NewMessage(pattern=r'/voice'))
    async def voice_to_text(event):
        """Розпізнає голосове повідомлення та конвертує в текст"""
        if not event.is_reply:
            await event.reply("❌ Використовуйте цю команду у відповіді на голосове повідомлення")
            return
        
        try:
            status.commands_processed += 1
            print(f"Processing /voice command from user {event.sender_id}")
            
            reply_message = await event.get_reply_message()
            
            if not reply_message.voice:
                await event.reply("❌ Це не голосове повідомлення")
                return
            
            await event.reply("🎤 Обробляю голосове повідомлення...")
            
            # Створюємо тимчасову директорію
            with tempfile.TemporaryDirectory() as temp_dir:
                # Завантажуємо голосове повідомлення
                voice_file = await reply_message.download_media(file=temp_dir)
                
                # Конвертуємо OGG в WAV за допомогою ffmpeg
                wav_file = os.path.join(temp_dir, 'audio.wav')
                
                try:
                    # Використовуємо subprocess замість os.system для кращої безпеки
                    subprocess.run([
                        'ffmpeg', '-i', voice_file, '-ar', '16000', 
                        wav_file, '-y'
                    ], check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    await event.reply("❌ Помилка конвертації аудіо. Переконайтесь, що ffmpeg встановлено.")
                    return
                except FileNotFoundError:
                    await event.reply("❌ ffmpeg не знайдено. Встановіть ffmpeg для роботи з голосовими повідомленнями.")
                    return
                
                # Розпізнаємо мову
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(wav_file) as source:
                        audio_data = recognizer.record(source)
                except Exception as e:
                    await event.reply(f"❌ Помилка читання аудіофайлу: {str(e)}")
                    return
                
                # Спробуємо розпізнати мову в різних мовах
                languages = [
                    ('uk-UA', 'українська'),
                    ('ru-RU', 'російська'),
                    ('en-US', 'англійська')
                ]
                
                recognized = False
                for lang_code, lang_name in languages:
                    try:
                        # Використовуємо метод recognize_google з speech_recognition
                        text = recognizer.recognize_google(audio_data, language=lang_code)
                        await event.reply(f"📝 Розпізнаний текст ({lang_name}):\n\n{text}")
                        recognized = True
                        break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        await event.reply(f"❌ Помилка сервісу розпізнавання: {e}")
                        return
                    except Exception as e:
                        continue
                
                if not recognized:
                    await event.reply("❌ Не вдалося розпізнати мову в голосовому повідомленні")
                    
        except Exception as e:
            error_msg = f"❌ Помилка: {str(e)}"
            status.last_error = error_msg
            print(f"Error in voice command: {e}")
            await event.reply(error_msg)

    @client.on(events.NewMessage)
    async def auto_reactions_and_responses(event):
        """Автоматичні реакції та відповіді"""
        if not event.text:
            return
        
        try:
            status.messages_processed += 1
            message_text = event.text.lower()
            
            # Перевіряємо наявність ключових слів для реакції ❤️‍🔥
            original_text = event.text  # Зберігаємо оригінальний текст для порівняння з @ символами
            for keyword in KEYWORDS_FOR_HEART:
                # Перевіряємо в нижньому регістрі для звичайних слів
                if keyword.startswith('@'):
                    # Для нікнеймів з @ перевіряємо і в оригінальному тексті, і без @
                    if keyword.lower() in message_text or keyword[1:].lower() in message_text:
                        found_keyword = keyword
                    else:
                        continue
                else:
                    # Для звичайних слів перевіряємо в нижньому регістрі  
                    if keyword.lower() in message_text:
                        found_keyword = keyword
                    else:
                        continue
                
                # Якщо знайшли збіг - надсилаємо реакцію
                try:
                    await client(functions.messages.SendReactionRequest(
                        peer=event.chat_id,
                        msg_id=event.id,
                        reaction=[types.ReactionEmoji(emoticon='❤️‍🔥')],
                        big=False,
                        add_to_recent=True
                    ))
                    status.reactions_sent += 1
                    print(f"Sent heart reaction for keyword: {found_keyword} (found in: '{event.text[:50]}...')")
                    break
                except Exception as e:
                    print(f"Failed to send reaction for {found_keyword}: {e}")
                    pass  # Ігноруємо помилки з реакціями
            
            # Відповідь на "Слава Україні"
            if 'слава україні' in message_text:
                await event.reply('Героям слава!')
                print("Responded to 'Слава Україні'")
            
            # Відповідь на згадування "Путін"
            if 'путін' in message_text:
                await event.reply('Путін хуйло')
                print("Responded to 'Путін'")
                
        except Exception as e:
            print(f"Error in auto reactions: {e}")
            status.last_error = str(e)

    @client.on(events.NewMessage(pattern=r'/status'))
    async def bot_status(event):
        """Показує статус бота"""
        try:
            status_text = f"""
🤖 **Статус Userbot**

📊 **Статистика:**
• Команд оброблено: {status.commands_processed}
• Реакцій надіслано: {status.reactions_sent}
• Повідомлень оброблено: {status.messages_processed}

🔧 **Доступні команди:**
• `/gayporn` або `/random` - випадкове повідомлення з каналу
• `/voice` (у відповіді на голосове) - конвертація в текст
• `/status` - цей статус

🔥 **Автоматичні функції:**
• Реакція ❤️‍🔥 на ключові слова
• Відповідь на "Слава Україні"
• Відповідь на згадування "Путін"
            """
            
            if status.last_error:
                status_text += f"\n⚠️ **Остання помилка:** {status.last_error}"
            
            await event.reply(status_text)
            
        except Exception as e:
            await event.reply(f"❌ Помилка отримання статусу: {str(e)}")

    print("✅ All handlers registered successfully")
    return status
