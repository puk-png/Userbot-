#!/usr/bin/env python3
"""
Скрипт для першої авторизації Telegram Userbot
Запустіть цей скрипт для налаштування авторизації перед основним ботом
"""

import asyncio
import os
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER, PASSWORD, SESSION_NAME

async def setup_authentication():
    """Налаштування авторизації Telegram"""
    print("🔐 Налаштування авторизації Telegram Userbot")
    print("=" * 50)
    
    # Створюємо клієнт
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        # Підключаємося
        await client.connect()
        print("✅ Підключено до Telegram")
        
        # Перевіряємо авторизацію
        if await client.is_user_authorized():
            print("✅ Ви вже авторизовані!")
            me = await client.get_me()
            username = getattr(me, 'username', 'немає')
            first_name = getattr(me, 'first_name', 'Невідомий користувач')
            print(f"👤 Авторизований як: {first_name} (@{username})")
            return True
        
        print(f"📱 Надсилаємо код підтвердження на: {PHONE_NUMBER}")
        
        # Надсилаємо код
        await client.send_code_request(PHONE_NUMBER)
        
        # Запитуємо код у користувача
        print("📲 Перевірте SMS або Telegram Desktop/Mobile")
        code = input("Введіть код підтвердження: ").strip()
        
        try:
            # Авторизуємося з кодом
            await client.sign_in(PHONE_NUMBER, code)
        except Exception as e:
            if "Two-step verification" in str(e) or "password" in str(e).lower():
                print("🔒 Потрібен пароль двофакторної автентифікації")
                password = PASSWORD or input("Введіть пароль: ").strip()
                await client.sign_in(password=password)
            else:
                raise e
        
        # Перевіряємо успішну авторизацію
        if await client.is_user_authorized():
            me = await client.get_me()
            username = getattr(me, 'username', 'немає')
            first_name = getattr(me, 'first_name', 'Невідомий користувач')
            print(f"✅ Успішно авторизовані як: {first_name} (@{username})")
            print(f"💾 Сесія збережена як: {SESSION_NAME}.session")
            return True
        else:
            print("❌ Помилка авторизації")
            return False
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False
    finally:
        try:
            if client.is_connected():
                await client.disconnect()
        except:
            pass

async def main():
    """Головна функція"""
    success = await setup_authentication()
    
    if success:
        print("\n🎉 Авторизація завершена успішно!")
        print("▶️  Тепер можете запустити основного бота командою:")
        print("   python main.py")
    else:
        print("\n❌ Авторизація не вдалася")
        print("💡 Спробуйте ще раз або перевірте налаштування")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Скасовано користувачем")
    except Exception as e:
        print(f"❌ Критична помилка: {e}")