import asyncio
import os
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER, PASSWORD, SESSION_NAME
from bot_handlers import register_handlers
from web_dashboard import start_web_server
import threading

async def main():
    """Основна функція запуску"""
    print("🚀 Запуск Telegram Userbot...")
    
    # Створюємо клієнт
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        # Підключаємося до Telegram
        await client.connect()
        print("🔗 Підключено до Telegram")
        
        # Перевіряємо авторизацію
        if not await client.is_user_authorized():
            print(f"📱 Надсилаємо код підтвердження на номер: {PHONE_NUMBER}")
            print("📬 Перевірте SMS або Telegram Desktop/Mobile")
        
        # Запускаємо процес авторизації з інтерактивним вводом коду
        try:
            def code_callback():
                print("📲 Введіть код підтвердження з SMS або Telegram:")
                code = input("Код: ")
                return code
            
            def password_callback():
                return PASSWORD
            
            await client.start(phone=PHONE_NUMBER, code_callback=code_callback, password=password_callback)
        except Exception as auth_error:
            print(f"❌ Помилка авторизації: {auth_error}")
            print("💡 Спробуйте видалити файл {SESSION_NAME}.session і запустити знову")
            return
        
        # Отримуємо інформацію про користувача
        me = await client.get_me()
        username = getattr(me, 'username', 'немає')
        first_name = getattr(me, 'first_name', 'Невідомий користувач')
        print(f"✅ Успішно увійшли як: {first_name} (@{username})")
        
        # Реєструємо обробники подій
        bot_status = register_handlers(client)
        bot_status.is_running = True
        
        print("🎯 Userbot успішно запущено!")
        print("\n📋 Доступні команди:")
        print("• /gayporn або /random - випадкове повідомлення з каналу")
        print("• /voice (у відповіді на голосове) - конвертація голосу в текст")
        print("• /status - показати статус бота")
        print("\n🤖 Автоматичні функції:")
        print("• Реакція ❤️‍🔥 на ключові слова")
        print("• Відповідь на 'Слава Україні' → 'Героям слава!'")
        print("• Відповідь на згадування 'Путін' → 'Путін хуйло'")
        print(f"\n🌐 Веб-дашборд доступний на: http://localhost:5000")
        
        # Запускаємо веб-сервер в окремому потоці
        web_thread = threading.Thread(target=start_web_server, args=(bot_status,))
        web_thread.daemon = True
        web_thread.start()
        
        # Запускаємо бота
        await client.run_until_disconnected()
        
    except KeyboardInterrupt:
        print("\n⏹️ Зупинка бота...")
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        print("💡 Спробуйте видалити файл {SESSION_NAME}.session і запустити знову")
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
        print("\n⏹️ Програма перервана користувачем")
    except Exception as e:
        print(f"❌ Помилка запуску: {e}")
