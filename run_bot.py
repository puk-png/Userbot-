#!/usr/bin/env python3
"""
Простий запуск бота після авторизації
"""

import asyncio
import os
from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME
from bot_handlers import register_handlers
from web_dashboard import start_web_server
import threading

async def main():
    """Запуск бота після авторизації"""
    print("🚀 Запуск Telegram Userbot...")
    
    # Перевіряємо наявність файлу сесії
    if not os.path.exists(f"{SESSION_NAME}.session"):
        print("❌ Файл сесії не знайдено!")
        print("📝 Спочатку запустіть: python setup_auth.py")
        return
    
    # Створюємо клієнт
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        # Підключаємося
        await client.connect()
        print("🔗 Підключено до Telegram")
        
        # Перевіряємо авторизацію
        if not await client.is_user_authorized():
            print("❌ Не авторизовано!")
            print("📝 Запустіть: python setup_auth.py")
            return
        
        # Отримуємо інформацію про користувача
        me = await client.get_me()
        username = getattr(me, 'username', 'немає')
        first_name = getattr(me, 'first_name', 'Невідомий користувач')
        print(f"✅ Увійшли як: {first_name} (@{username})")
        
        # Реєструємо обробники
        bot_status = register_handlers(client)
        bot_status.is_running = True
        
        print("🎯 Userbot запущено!")
        print("\n📋 Доступні команди:")
        print("• /gayporn або /random - випадкове повідомлення з каналу")
        print("• /voice (у відповіді на голосове) - конвертація голосу в текст")
        print("• /status - показати статус бота")
        print("\n🤖 Автоматичні функції:")
        print("• Реакція ❤️‍🔥 на ключові слова")
        print("• Відповідь на 'Слава Україні'")
        print("• Відповідь на згадування 'Путін'")
        print(f"\n🌐 Веб-дашборд: http://localhost:5000")
        
        # Запускаємо веб-сервер
        web_thread = threading.Thread(target=start_web_server, args=(bot_status,))
        web_thread.daemon = True
        web_thread.start()
        
        # Запускаємо бота
        await client.run_until_disconnected()
        
    except KeyboardInterrupt:
        print("\n⏹️ Зупинка бота...")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    finally:
        try:
            if client.is_connected():
                await client.disconnect()
        except:
            pass
        print("👋 Userbot зупинено")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Перервано користувачем")
    except Exception as e:
        print(f"❌ Помилка запуску: {e}")